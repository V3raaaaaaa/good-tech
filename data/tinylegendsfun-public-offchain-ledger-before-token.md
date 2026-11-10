---
name: "Counting house" publik buat poin off-chain sebelum token ada
category: data
project: Tiny Legends (tinylegends.fun)
chain: Solana (devnet, planned)
tags: [transparency, points, emission, burn, pre-token]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://tiny-legends-production.up.railway.app/api/v1/grit/status
---
# "Counting house" publik buat poin off-chain sebelum token ada

## Ringkas
Mata uang game (GRIT) masih off-chain, tapi tim udah buka endpoint publik tanpa auth plus halaman `/grit` yang nunjukin supply cap, emisi yang dijadwalin sampe hari ini, total minted/burned/held/treasury, dan rate harian `gritPerPoint` per hari. Bagian `chain` sengaja `null` sampe token beneran di-deploy.

## Kenapa bagus
- Pemain bisa ngecek inflasi sendiri: `scheduledToDateGrit` (32,85M) vs `mintedGrit` (2,48M) nunjukin emisi aktual jauh di bawah jadwal.
- Sink keliatan: `burnedGrit` 2,27M dari 2,48M minted (~92% balik kebakar lewat toko).
- Schema-nya udah nyiapin field on-chain (`burnSettledOnChainGrit`, `withdrawnGrit`, `depositedGrit`, dan di `chain`: `mintAuthorityRemoved`, `miningVaultGrit`, `teamGrit`, `liquidityGrit`, `treasuryGrit`, `withdrawalFloatGrit`). Waktu token live, angka off-chain sama on-chain bisa dicocokin di satu halaman.
- Rate harian dengan flag `nearCeiling`/`ceilingReached` (di `/api/v1/store`) = emisi dibatasin anggaran harian, bukan per-aksi tanpa batas.

## Cara kerja
- `GET /api/v1/grit/status` → `{supply:{totalGrit, miningCapGrit, scheduledToDateGrit}, game:{mintedGrit, burnedGrit, treasuryGrit, pointsPlayed, heldByPlayersGrit, ...}, days:[{day, gritPerPoint, mintedGrit, burnedGrit, points}], chain:null}`.
- Halaman publik nge-poll tiap 30 detik, dan pause kalo `document.hidden`.
- Data sample di bundle nunjukin rencana alokasi: total 1B, mining vault ~80%, treasury 10%, liquidity ~5%, team 5%, mint authority dicabut. **Ini sample UI, bukan komitmen.**

## Cara pakai di project gw
- Project poin/airdrop: publish ledger agregat harian dari hari pertama, jangan nunggu TGE.
- Pake schema yang sama buat fase off-chain dan on-chain biar rekonsiliasi gampang.
- Tampilin "dijadwalin vs beneran di-mint" biar orang gak bisa nuduh diam-diam inflasi.

## Caveat / jangan ditiru
- Angka-angkanya dilaporin sendiri sama server, gak ada bukti kriptografis. Ini transparansi, belum verifikasi. Tambahin merkle root harian kalo mau bisa diaudit.
- Alokasi di sample UI belum ada di kontrak mana pun.

## Bukti
- https://tiny-legends-production.up.railway.app/api/v1/grit/status
- https://tiny-legends-production.up.railway.app/grit ("GRIT Counting House · Devnet")
- https://tiny-legends-production.up.railway.app/api/v1/store (`rate.gritPerPoint`, `nearCeiling`, `ceilingReached`)
