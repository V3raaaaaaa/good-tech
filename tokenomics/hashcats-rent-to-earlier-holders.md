---
name: Rent ke holder epoch sebelumnya
category: tokenomics
project: Hashcats (hashcats.fun)
chain: RobinHoodChain 4663
tags: [nft, revenue-share, epoch, price-curve]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-09-12
---

# Rent ke holder epoch sebelumnya

## Ringkas
Tiap mint baru bayar "rent" kecil ke semua NFT yang dimint di epoch sebelumnya. Holder awal dapet income dari mint selanjutnya.

## Kenapa bagus
- Insentif buat mint awal + hold, tanpa token reward terpisah.
- Pembayaran on-chain murni, gak butuh distributor off-chain.

## Cara kerja
- Harga = `PRICE_STEP (0.00002) × jumlah cat sebelum epoch sekarang`, jadi dobel tiap epoch.
- Ukuran epoch 8, 16, 32 … 8192 (total 16376).
- Tiap cat dapet `RENT_STEP = 0.000014 ETH` per mint di epoch yang *lebih akhir* (strictly later).
- Break-even ≈ 354 mint setelahnya; full run ≈ 0.22 ETH per cat.
- Burn cat → 1000 $HASH setelah 600 s (exit ramp ke token).

## Cara pakai di project gw
Pola "pay-it-back" ini cocok buat koleksi yang mau reward early minter. Pakai accumulator per-share (kayak MasterChef `accRentPerShare`) biar O(1) per mint, jangan loop ke semua holder.

## Caveat / jangan ditiru
- Harga eksponensial = ponzi-shaped: epoch akhir bayar rent ke semua yang awal, dan bakal sepi. Pakai kurva lebih landai kalau mau tahan lama.
- Rent cuma jalan selama ada mint baru. Begitu mint berhenti, income nol.

## Bukti
- Contract: `0xca75df55cc9c476db27a7375d1fc8e794cf80721` (RHC 4663)
