---
name: Rebate Dutch auction + GTD merkle + trading lock
category: contracts
project: Yield Fields
chain: Robinhood Chain (4663)
tags: [nft-mint, dutch-auction, merkle, erc721a, erc721c, refund]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, Founding Deeds 0x231142E88f523B0a4F46D2D79FAAB2cE1828E43a (Robinhood Chain), https://yieldfields.fun/api/mint/state, ABI di bundle publik https://yieldfields.fun/_next/static/immutable/chunks/30n09xn9pzm7s.js
---
# Rebate Dutch auction + GTD merkle + trading lock

## Ringkas
Satu kontrak ERC721A punya 2 fase. Fase GTD: harga tetap 0.1 ETH, allowlist merkle dengan kuota per leaf. Fase publik: Dutch auction linear 1 ETH → 0.069 ETH dalam 24 jam, max 5 per wallet. Semua pembeli publik akhirnya bayar **harga clearing yang sama** (`finalPrice`), kelebihannya di-refund. Transfer dikunci sampai owner manggil `enableTrading()`.

## Kenapa bagus
- Nggak ada gas war yang bikin pembeli awal rugi. Siapa pun yang bayar lebih tinggi di awal dapet rebate ke harga akhir.
- `claimRefund(address buyer)` permissionless: siapa aja bisa trigger refund buat buyer mana pun, dan dananya selalu ke buyer.
- Trading lock bikin nggak ada flip/listing murah selama mint jalan, jadi price discovery DA nggak keganggu.
- `/api/mint/state` publik nge-expose semua parameter (gtdRoot, start/floor/final price, minted) dengan `blockNumber` + `blockHash`, jadi bisa dicocokin sama chain.

## Cara kerja
- Konstanta: `GTD_PRICE`, `PUBLIC_START_PRICE`, `PUBLIC_END_PRICE`, `*_TIMESTAMP`, `DA_MAX_PER_WALLET`, `TEAM_RESERVE` (dimint ke deployer di constructor via ERC2309).
- `gtdMint(qty, allocatedQty, proof)`: leaf = (address, allocatedQty), bisa claim sebagian.
- `publicMint(qty)`: bayar `getCurrentPrice()`, dicatat `paidOf[buyer]`. Mint terakhir yang bikin sold out nge-set `finalPrice`.
- `refundOf(buyer) = paidOf − qty × finalPrice`. `claimRefund` cuma jalan setelah sold out atau DA selesai (error `NotSoldOut`).
- `withdraw(to)` cuma bisa narik bagian yang bukan refund (`withdrawn()` dicatat).
- Hasil nyata: public 975 deed sold out 29 detik, clearing 0.999687 ETH. 306 refund total 0.136 ETH, `withdrawn` 1,208.495 ETH.

## Cara pakai di project gw
- Pakai ERC721A + Solady OwnableRoles, simpan `paidOf`/`qtyOf` per buyer, `finalPrice` diset saat token terakhir dimint atau waktu habis.
- Expose endpoint read-only "mint state" yang nyantumin block number/hash biar frontend dan user bisa verifikasi.
- Kunci transfer sampai sold out (`tradingEnabled` flag di `_beforeTokenTransfers`, kecuali mint).

## Caveat / jangan ditiru
- Kalau demand tinggi banget, DA langsung sold out di harga start, jadi praktis bukan "discovery". Pertimbangin start price lebih tinggi atau durasi decay lebih pendek.
- Di sini `enableTrading` dan `withdraw` dipegang EOA deployer selama mint. Mending owner multisig dari awal.
- Source nggak di-verify, jadi detail rumus refund disimpulkan dari ABI + angka on-chain.

## Bukti
- `MAX_SUPPLY=3333`, `GTD_PRICE=0.1 ETH`, `PUBLIC_START_PRICE=1 ETH`, `PUBLIC_END_PRICE=0.069 ETH`, `finalPrice=999687511574074075`, `publicMinted=975`, `withdrawn=1208.495 ETH` (eth_call ke 0x231142E88f523B0a4F46D2D79FAAB2cE1828E43a).
- Event `Minted` fase 1: blok 87709107 → 87709394 (2026-10-13 18:00:00–18:00:29 UTC). `TradingEnabled` tx 0xa2efa8464dc7c819f8c08f0d59b1ad4720614a765c42f8a9ee6d9d993ecc0d2d.
- https://yieldfields.fun/api/mint/state
