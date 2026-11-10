---
name: Staking escrow dengan ETH backing per-NFT (bobot fertility) + unstake tetap jalan saat pause
category: contracts
project: Yield Fields
chain: Robinhood Chain (4663)
tags: [nft-staking, backing, burn-to-redeem, pause, erc7201, uups]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, Deed staking 0x0AcFcD1483686fcd94DABeA03714321d0E05fc8D (Robinhood Chain), https://yieldfields.fun/docs/deed-gameplay/the-root-cellar, https://yieldfields.fun/docs/deed-gameplay/staking-and-the-fert-deck
---
# Staking escrow dengan ETH backing per-NFT (bobot fertility) + unstake tetap jalan saat pause

## Ringkas
Fee "build" (0.01 ETH per Fert Deck) nggak masuk ke tim, tapi ditahan di kontrak staking sebagai `backing`. Tiap NFT punya klaim pro-rata ke backing itu sesuai `fertility` (5–9), dan klaimnya cuma bisa dicairkan dengan **burn** NFT yang di-stake (`burnAndRedeemEth(ids, minEthOut)`). Pause kontrak nge-blok aksi masuk (build, dll) tapi **unstake tetap bisa**.

## Kenapa bagus
- Bikin floor "intrinsic" yang naik seiring aktivitas, dan tiap burn bikin sisa holder dapet porsi lebih gede.
- `minEthOut` / `minYieldOut` di burn = proteksi slippage kalau ada burn lain di blok yang sama.
- Exit selalu terbuka walau pause: pause jadi alat safety, bukan alat sandera.
- Fertility per token di-set sekali lalu dikunci (`fertilityComplete` → `FertilityLocked`), jadi bobot nggak bisa diutak-atik.
- `recoverDeed` cuma buat NFT nyasar, ada guard `NotRecoverable` buat yang di-stake.

## Cara kerja
- `backing()` = 31.1 ETH = 3,110 deck × 0.01 ETH (= balance kontrak). `totalFertility()` = 19,773 (semua 3,333 deed, staked atau nggak).
- `redeemValue([id]) = backing × fertility(id) / totalFertility` → Common (5) = 0.00786 ETH sekarang.
- Burn butuh `BURNER_ROLE` di kontrak NFT; saat ini belum di-grant, jadi `burnAndRedeemEth` revert `Unauthorized` (fitur belum dibuka).
- Storage ERC-7201 (slot paused/config di `0x98a9fa1e…2b00`), Solady UUPS.
- Simulasi `eth_call` dengan state override `paused=true`: `unstake([1])` dari staker sukses, `buildStructure` revert `Paused()`.

## Cara pakai di project gw
- Arahin fee aksi in-game ke vault backing on-chain, bukan ke treasury, kalau mau NFT punya floor yang bisa diverifikasi.
- Pisahin modifier: `whenNotPaused` di entry (stake/build/claim), **jangan** di `unstake`/withdraw.
- Bobot tetap per token (rarity) + lock setelah semua diset.
- Selalu kasih `minOut` di fungsi redeem.

## Caveat / jangan ditiru
- UUPS tanpa timelock: owner bisa upgrade dan ngubah semua jaminan di atas. Kalau niru, pasang timelock/upgrade delay.
- Source belum verified; perilaku dibuktikan lewat simulasi, bukan review kode.
- Docs FAQ project ini malah bilang unstake nunggu unpause (nggak sesuai kontrak), jadi sinkronin docs sama kode.

## Bukti
- eth_call ke 0x0AcFcD1483686fcd94DABeA03714321d0E05fc8D: `backing()=31.1e18`, `totalFertility()=19773`, `fertilityComplete()=true`, `structureFee(1)=0.01e18`, `CLAIM_FEE_BPS=1000`, `claimFeeSplit()=(500,500)`.
- Event: 3,147 `DeedStaked`, 105 `DeedUnstaked`, 3,110 `DeedStructureBuilt`, 1,199 `BackingReceived`.
- Error selector: `NotRecoverable` 0x455c9353, `FertilityLocked` 0x076cc28c, `Paused` 0x9e87fac8.
