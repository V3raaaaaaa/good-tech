---
name: Tax token yang dikonfigurasi creator lewat hook Uniswap v4 (cash/reflection/burn/pair)
category: contracts
project: vibe/vibe (Seedify)
chain: Robinhood Chain Testnet 46630
tags: [uniswap-v4, hook, tax, reflection, buyback, tokenomics, launchpad]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, `v6_all.json` (snapshot recon)
---

# Tax token yang dikonfigurasi creator lewat hook Uniswap v4 (cash/reflection/burn/pair)

## Ringkas
Pas launch, creator milih tax trading (1/2/3%) dan cara bagi hasilnya: ke treasury project (cash), reflection ke holder (token), burn, atau holder dapet pair currency (ETH). Satu hook v4 yang sama ngejalanin ini di curve dan setelah graduate.

## Kenapa bagus
- Satu parameter set (`taxBps` + `weights`) nentuin tokenomics per token. Gak perlu deploy kontrak tax custom (yang biasanya jadi sumber honeypot).
- Tax diambil di hook (beforeSwap/afterSwap), bukan di `transfer`, jadi transfer biasa gak kena tax dan wallet/aggregator gak rusak.
- Reflection pakai pola accumulator (`rewardMark`, `pendingReward`, `claimFor`, `claimMany`, `settleReward`), bukan loop holder, jadi gas-nya O(1).
- `holdersPairBps` = holder dapet ETH beneran dari volume, bukan token sendiri yang diinflasi.
- Protokol ambil bagian tetap dari tax (20%) → sebagian buat buyback token platform ke holder, sebagian buat referral (25% dari yang ditahan, seumur hidup).

## Cara kerja
```
launch(params: taxBps ∈ {100,200,300}, weights{cashBps, holdersBps, burnBps, holdersPairBps} sum 10000)
hook.afterSwap: tax = amount * taxBps
  protocol 20%  -> buyback VIBE (80%) + retained (20%; referrer 25% dari ini)
  project  80%  -> cash ke projectTreasury | rewards ke holder | burn | pair ke holder
token.excludedBalance / isExcludedFromRewards: curve, pool, locker gak ikut dapet reflection
```
Data nyata (2050 launch V6): tax 1% dipilih 66%, 2% 30%, 3% 4%.

## Cara pakai di project gw
Kalau bikin launchpad di chain dengan Uniswap v4: satu hook buat semua token, parameter per pool disimpan di `pools(bytes32)`. Kasih creator preset bobot, jangan input bebas. Reflection pakai accumulator per share + exclude kontrak sistem.

## Caveat / jangan ditiru
- Hook v4 harus di address dengan bit permission yang pas (salt mining CREATE2).
- Reflection butuh `claim`, dan holder yang gak klaim = saldo nganggur di kontrak.
- Tax di hook cuma kena kalau trading lewat pool yang punya hook itu, makanya mereka butuh venue allowlist (lihat [vibevibe-transfer-lock-venue-allowlist](vibevibe-transfer-lock-venue-allowlist.md)).
- Unverified: bobot dan alur dibaca dari API + selector, bukan source.

## Bukti
- Hook `0xE61e46724BA5DEC31f2be031106558774A65e8ec` (selector: semua callback v4, `pools(bytes32)`, `protocolOwed`, `flushProtocol`)
- Token selector: `pendingReward`, `claimFor`, `claimMany`, `rewardHolders`, `isExcludedFromRewards`, `onFee`
- Bundle: "V6 base tax: 20% protocol share × 20% retained × 25% commission = 1% of the trading tax"
