---
name: Throttle emisi berbasis supply beredar + penalti per-exporter
category: tokenomics
project: Yield Fields
chain: Robinhood Chain (4663)
tags: [emission, anti-dump, game-economy, rate-limit, public-metrics]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://yieldfields.fun/api/fert-rate, https://yieldfields.fun/docs/deed-gameplay/fertilizer
---
# Throttle emisi berbasis supply beredar + penalti per-exporter

## Ringkas
Resource yang diproduksi NFT (Fertilizer) belum ada sink-nya sampai farming buka. Biar nggak numpuk, tiap jam server ngitung **supply beredar vs target (7 hari output network)** dan nurunin kecepatan semua produsen kalau kelebihan. Ditambah penalti per wallet kalau wallet itu nge-export (bawa ke market) terlalu banyak dibanding output-nya.

## Kenapa bagus
- Emisi nyesuain diri ke demand nyata tanpa harus ganti angka manual.
- Ada floor (50%), jadi produsen nggak pernah dimatiin total, dan resource yang udah dipegang nggak pernah diambil.
- Penalti exporter nyasar ke perilaku dump (farm → jual), bukan ke yang nyimpen/pakai.
- Angkanya publik di endpoint JSON, jadi semua orang bisa liat kondisi throttle.

## Cara kerja
- Network rate: kalau circulating > 7 hari output → deck melambat; 10 hari = 70%, ≥14 hari = 50% (floor `floorBps 5000`). Update tiap jam (`hour`, `nextUpdateAt`).
- Exporter rate: kalau satu wallet export > 25% output harian deck-nya dalam 24 jam → 90% di 30%, 70% di 40%, 50% di ≥50%. Pulih sendiri setelah export lewat 24 jam. Import balik nggak ngapus hitungan export.
- Deck jalan di `min(networkRate, exporterRate)`.
- Endpoint: `{"supply":50809,"target":63199.5,"networkBps":10000,"floorBps":5000,"targetDays":7,"usedTotal":0,"claimedTotal":50809,...}`. Target 63,199.5 = 7 × 9,028.5/hari = output dari total fertility deck yang aktif.
- Kalau sumber data basi, export di-pause ("If the game can't check your limit, export pauses until it can") — fail-closed.

## Cara pakai di project gw
- Hitung `targetSupply = targetDays × dailyOutput`, simpan `rateBps` per jam di DB, apply ke produksi berikutnya (bukan retroaktif).
- Publish endpoint read-only metrik ekonomi (supply, target, rate, cause, sourceAge).
- Bedain "hold" vs "export": penalti cuma buat aliran keluar ke market.

## Caveat / jangan ditiru
- Semua off-chain: user harus percaya server ngitung jujur. Kalau bisa, commit snapshot per jam (hash) on-chain.
- Penalti per wallet gampang diakalin pakai banyak wallet. Di sini dibatasi karena output ikut jumlah deck per wallet.
- Rumus bisa diganti tim kapan aja ("launch settings and may change").

## Bukti
- https://yieldfields.fun/api/fert-rate (GET publik, 2026-11-10).
- Aturan lengkap: https://yieldfields.fun/docs/deed-gameplay/fertilizer.
