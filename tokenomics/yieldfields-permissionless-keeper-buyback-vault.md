---
name: Buyback vault permissionless (keeper reward, rate harian, 1 buy per blok, price guard)
category: tokenomics
project: Yield Fields
chain: Robinhood Chain Testnet (46630)
tags: [buyback, keeper, twap, mev, treasury]
score: 7
status: claimed
added: 2026-11-11
source: recon 2026-11-11, ABI di bundle publik https://yieldfields.fun/_next/static/immutable/chunks/1s_78nxc0fu1-.js, BuybackVault testnet 0x86921aDeAb3252FfB0EF0096f3be138348084e8a
---
# Buyback vault permissionless (keeper reward, rate harian, 1 buy per blok, price guard)

## Ringkas
Vault nampung ETH (fee game) dan siapa aja boleh manggil `buy()` buat nge-buyback token dari pool. Yang manggil dapet reward kecil. Jumlah yang bisa dibelanjain dibatasi persentase per hari, maksimal per call, sekali per blok, dan ditolak kalau harga lompat terlalu jauh dari buy terakhir. Token hasil buyback dikirim ke reward pool (Truffle Pool), bukan ke tim.

## Kenapa bagus
- Buyback otomatis tanpa bot tim dan tanpa key: insentif `CALLER_REWARD_BPS` bikin keeper publik yang jalanin.
- Spend kayak DCA/TWAP (`DAILY_RATE_BPS`), jadi nggak ada satu buy besar yang bisa di-sandwich.
- `AlreadyBoughtThisBlock` + `PriceGuard` bikin manipulasi harga dalam satu blok nggak worth.
- Transparan: `spendable()`, `lastBuyPrice`, `totalSentToTruffles` publik.

## Cara kerja
- Konstanta testnet: `CALLER_REWARD_BPS=10` (0.1%), `DAILY_RATE_BPS=400` (4% saldo/hari), `MAX_PER_CALL=1 ETH`, `PRICE_GUARD_BPS=200` (2%).
- `buy()`: hitung `spendable` dari waktu sejak `lastBuyAt` × rate, cap `MAX_PER_CALL`; revert `NothingToSpend` / `AlreadyBoughtThisBlock` / `PriceGuard`; swap ke pool; kirim token ke `trufflePool`; bayar reward ke caller; emit `Buyback`.
- Immutable (constructor `yield_, pool_, trufflePool_`), nggak ada owner di ABI.

## Cara pakai di project gw
- Pakai buat program buyback treasury: vault immutable, rate harian kecil, reward keeper 5–20 bps, guard harga vs buy terakhir (atau vs TWAP oracle).
- Tujuan token: burn atau reward pool, jangan ke wallet tim.

## Caveat / jangan ditiru
- Baru ada di testnet; versi mainnet belum deploy, jadi status **claimed**.
- Guard "vs last buy price" bisa di-grind pelan-pelan (geser harga 2% tiap blok). Lebih kuat kalau dibandingin TWAP pool.
- Reward keeper harus lebih gede dari gas, kalau nggak nggak ada yang manggil.

## Bukti
- ABI `CALLER_REWARD_BPS, DAILY_RATE_BPS, MAX_PER_CALL, PRICE_GUARD_BPS, buy, lastBuyAt, lastBuyBlock, lastBuyPrice, spendable, totalSentToTruffles` + error `AlreadyBoughtThisBlock, NothingToSpend, PriceGuard` di bundle publik.
- eth_call testnet 46630 ke 0x86921aDeAb3252FfB0EF0096f3be138348084e8a: nilai konstanta di atas, `totalSentToTruffles` ≈ 1.62e21.
