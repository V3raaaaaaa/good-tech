---
name: Poin harian dipatok USD, dibayar dari pool harian pro-rata ("never pays more than the pool holds")
category: tokenomics
project: Tiny Legends
chain: Robinhood Chain 4663
tags: [p2e, reward-pool, oracle, pro-rata, emission-control, game-economy]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) (AB.EARN)
---

# Poin harian dipatok USD, dibayar dari pool harian pro-rata

## Ringkas
Pemain ngumpulin **poin**, bukan token. Tiap poin nilainya dipatok dalam USD (misal satu hari penuh di level 1 = $1.25), terus dikonversi ke token pakai harga oracle hari itu. Total yang dibayar per hari dibatasi pool harian: kalau pool kurang, semua poin dibayar lebih kecil (pro-rata), jadi game gak pernah bayar lebih dari isi pool.

## Kenapa bagus
- **Emisi gak ngebakar treasury pas token jatuh.** Ada batas atas token per poin (`LGND_PT`), jadi pas harga anjlok token per hari gak meledak.
- **Pro-rata ("Mint health")** = pool gak bisa minus. Dibanding P2E yang janji angka tetap, ini jujur soal batas.
- **First come first served + overflow 5%:** setelah pool habis, poin cuma dibayar 5% sampai reset harian. Ini ngerem farming massal di akhir hari.
- **Cap per akun** (rank, pack, totem, NFT) = earn sebanding sama komitmen, dengan bagian earn passive 50% / raid 25% / battle 25%.
- Semua pembayaran in-game → treasury otomatis split burn / reward pool, jadi ada sink yang langsung ngisi pool.
- Harga di toko dipatok USD (sen) dan ditagih dalam token pakai harga oracle, jadi harga barang stabil walau token naik turun.

## Cara kerja
```js
EARN = { DAY_USD: 1.25, USD_PT: 1/60, LGND_PT: 5000/60, OVERFLOW: 0.05, POOL_DIV:..., PRO_RATA: 1,
         SHARE: {passive: .5, raid: .25, battle: .25}, RANKS: [{wave, cap, usd}...] }
ptRate(lgndUsd) = min(LGND_PT, (DAY_USD/60) / lgndUsd)     // token per poin, dibatasi atas
payout_i = pts_i * ptRate * min(1, pool_today / Σ(pts * ptRate))
```
Server: `/price` (sumber + flag `stale`), `/earn/state` (pts, balance, today pool), settle harian di menit `SETTLE_MIN`.

## Cara pakai di project gw
Buat game/quest dengan reward token: kasih poin, bukan token langsung. Tentuin pool harian dari pemasukan nyata (fee/sink), bayar pro-rata, patok nilai poin ke USD dengan batas atas token. Tampilin "estimate, not a promise" kayak yang mereka lakuin.

## Caveat / jangan ditiru
- Di sini parameter (`earn.dayUsd`, `maxDayLgnd`) diubah live lewat admin panel: dari 1.25 ke 100 USD/hari setelah harga jatuh. Jadi aturan bisa berubah kapan aja. Kunci parameter di kontrak atau timelock.
- Pool yang diisi dari pembayaran pemain baru tetap ponzi-shaped. Pro-rata cuma bikin jatuhnya pelan.
- Poin dari hasil battle yang dilaporin client = farmable. Pool pro-rata cuma bagi rata kerugiannya ke pemain jujur.
- Harga oracle dari DexScreener pada pool $11k gampang dimanipulasi.

## Bukti
- `AB.EARN` di `game.js` (snapshot recon); string UI "A point is worth {0} USD in LGND at the day's price; when the pool is short every point pays less (Mint health)"
- `GET https://api.tinylegendsgame.io/config` → `{"earn.dayUsd":100,"earn.maxDayLgnd":1000000}`; `/price` → `{"lgndUsd":0.00001746,"src":"dexscreener","stale":false}`
