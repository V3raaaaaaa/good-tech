---
name: Buyback oleh keeper dengan batas on-chain + ganti treasury 2 langkah
category: security
project: vibe/vibe (Seedify)
chain: Robinhood Chain Testnet 46630
tags: [keeper, buyback, burn, timelock, treasury, admin-limits]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, `selectors.json` (snapshot recon)
---

# Buyback oleh keeper dengan batas on-chain + ganti treasury 2 langkah

## Ringkas
Buyback token (VIBE, SFUND) dijalanin bot keeper biar timing-nya fleksibel, tapi kontraknya sendiri yang ngebatesin keeper: ada cooldown, blackout, max price impact, max porsi budget per run, dan hasilnya dikirim ke burn address yang gak bisa diambil. Policy-nya mereka sebut "keeper-authorized-with-external-limits".

## Kenapa bagus
- Keeper bisa aja dibobol, tapi yang bisa dia lakuin cuma beli sesuai aturan. Gak bisa nguras budget sekaligus atau beli di harga ngaco.
- Batasnya keliatan on-chain sebagai konstanta: `COOLDOWN` 300 s, `BLACKOUT` 6 jam, `MAX_IMPACT_BPS` 200 (2%), `MAX_SHARE_BPS` 50 (0.5% budget per run), `TREASURY_SHARE_BPS` 2000.
- Token hasil buyback: dikirim ke holder (`tokensToHoldersUnits`) atau di-burn ke `BURN_ADDRESS` (`irrecoverable-burn-address`). Gak masuk wallet tim.
- Ganti treasury di kontrak split SFUND pakai `proposeTreasury` → `acceptTreasury` (plus `cancelTreasuryProposal`), jadi gak bisa dipindah diam-diam dalam satu tx.
- `executeBuyback(amount, minOut, sqrtPriceLimitX96, deadline)` maksa keeper ngasih batas slippage dan deadline.

## Cara kerja
```
budget() bertambah dari porsi fee
keeper -> buyback.flush()/executeBuyback(...)
  require(now >= lastRun + COOLDOWN && !inBlackout)
  spend = min(arg, budget * MAX_SHARE_BPS / 1e4)
  swap di pool v4 dengan sqrtPriceLimit -> impact <= MAX_IMPACT_BPS
  20% ke treasury (treasuryOwed, ditarik terpisah), sisanya token ke holder / burn
```

## Cara pakai di project gw
Apapun yang dijalanin bot (buyback, rebalance, payout): kasih bot role minimal, terus taruh semua batas di kontrak sebagai konstanta immutable. Perubahan alamat penting (treasury, keeper) pakai propose/accept atau timelock.

## Caveat / jangan ditiru
- Keeper tetap bisa milih *kapan* beli dalam batas itu, jadi bisa front-run sendiri kalau keeper-nya nakal.
- Konstanta immutable = kalau salah set, harus deploy ulang.
- Keeper SFUND (`0xC997…7D29`) itu EOA dengan nonce 44k. Single key. Batas on-chain-nya yang bikin itu masih oke.
- Unverified: nama fungsi dari 4byte, nilai dari `cast call`.

## Bukti
- Buyback `0x7F030Eb56e8E09063929d1063f603232435E90f0`: `COOLDOWN()=300`, `BLACKOUT()=21600`, `MAX_IMPACT_BPS()=200`, `MAX_SHARE_BPS()=50`, `TREASURY_SHARE_BPS()=2000`
- SFUND split `0x3b13605865D7164d1dfe2080E22910df3a701899`: `proposeTreasury`, `acceptTreasury`, `cancelTreasuryProposal`, `executeBuyback(uint256,uint256,uint160,uint256)`, `BURN_ADDRESS()`
- `/api/v1/chains/46630/config`: `buybackDisposition: irrecoverable-burn-address`, `buybackExecutionModel: keeper-authorized-with-external-limits`
