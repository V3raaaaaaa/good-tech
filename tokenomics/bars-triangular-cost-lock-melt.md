---
name: NFT bernomor yang "dicetak" dari token: Bar #n mengunci n token, bisa dilebur balik
category: tokenomics
project: Bars (Jack Butcher / jack.art)
chain: Ethereum mainnet 1
tags: [nft, token-backed, sink, triangular-pricing, melt, vault-per-nft]
score: 7
status: claimed
added: 2026-11-11
source: jack.art/exchange/bars + ABI di /exchange/bars/mint.js (kontrak belum deploy saat recon)
---

# NFT bernomor yang "dicetak" dari token: Bar #n mengunci n token, bisa dilebur balik

## Ringkas
Bar #1 isinya 1 BALANCE, Bar #2 isinya 2, dst sampai 10,000. Tiap Bar punya vault kontrak sendiri yang megang tokennya. `melt` burn Bar dan balikin token ke owner. Nomor gak pernah dicetak ulang.

## Kenapa bagus
- **Floor value on-chain:** Bar #n selalu bisa dilebur jadi n token. Harga NFT ≥ nilai melt (kalau tidak, ada arb beli-lalu-lebur).
- **Sink token tanpa burn:** total N bar ngunci N(N+1)/2 token. 10,000 bar = 50,005,000 token, jadi cap efektif ditentukan supply yang beredar, bukan angka 10k.
- Harga naik linear per nomor, jadi nomor kecil murah + collectible, nomor besar mahal tapi tetap redeemable.
- Mint "up to": `mintUpTo(to, maxQuantity, maxTotal)` ngasih bar berikutnya selama muat di budget. Kalau ada yang nyalip, lu dapet nomor lebih besar/lebih sedikit, gak overpay.
- Helper `buyAndMint(maxQuantity, maxBalance, quotedBalance, deadline)` payable: swap ETH→token via pool v4 + mint dalam 1 tx, sisa ETH di-refund.
- Art on-chain `art(number, ink[4])`: nomor = deretan blok, lubang = digit, warna = ink token di dalam vault.

## Cara kerja (dari ABI)
- `mintListed(to, day, proof, maxQuantity, maxTotal)` sebelum `publicStart`; `LIST_CAP` per wallet; `MAX_BATCH` 10.
- `work(id) → (vault, amount, minter, block, melted, ink[4])`; `melt(id)`, `meltBatch(ids)`; `isMeltOpen()` (UI: baru buka setelah `mintEnd`).
- Event `MintBatch(payer, to, first, quantity, amount)`, `Melted(id, owner, amount)`.

## Cara pakai di project gw
Wrapper NFT untuk token sendiri: harga = nomor, vault per NFT, melt setelah window mint tutup. Cocok buat bikin demand token + NFT yang punya floor jelas.

## Caveat / jangan ditiru
- 1 vault per Bar = deploy kontrak + transfer token ke address baru tiap NFT. Di token dengan hook mahal (auto-mint wallet artwork) itu ~290k gas cuma buat transfernya.
- Lock sampai mint tutup (8 hari) = risiko harga token selama itu; melt balikin **jumlah** token, bukan nilai USD.
- Status `claimed`: source Bars belum verified saat recon.

## Bukti
- jack.art/exchange/bars (FAQ: "N Bars need N × (N + 1) ÷ 2 BALANCE")
- ABI string di `mint.js` (snapshot recon): `mintUpTo`, `mintListed`, `buyAndMint`, `quote`, `work`, `melt`, `meltBatch`, `isMeltOpen`
