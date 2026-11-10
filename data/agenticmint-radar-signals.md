---
name: Sinyal radar mint (deployer record, two-phase, timed, 72h outcome)
category: data
project: agenticmint.ai (Dr.OVG)
chain: BSC 56
tags: [radar, scoring, deployer, analytics]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-02 (v3.8.2)
---

# Sinyal radar mint (deployer record, two-phase, timed, 72h outcome)

## Ringkas
Set fitur yang bikin radar mint berguna, bukan cuma list: track record deployer, deteksi mint dua fase, mint terjadwal, dan hasil jual 72 jam.

## Kenapa bagus
- **Deployer record + block serial deployer**: satu sinyal paling kuat buat filter spam. Di BSC 48 owner pegang 4.627 dari 10.119 contract.
- **Two-phase detection**: free part + paid part di contract yang sama, dibaca dari getter.
- **Timed mints**: tangkap contract yang `saleStart` di masa depan, jadi bisa siap sebelum buka. Satu-satunya cara menang FCFS menit pertama.
- **72h secondary outcome**: ukur apakah mint kemarin beneran laku. Feedback loop buat scoring.
- Alasan skor ditampilin (scored reasons), bukan angka doang.

## Cara kerja
Public read API: `/api/state`, `/api/market`, `/api/collections`. Kita replikasi di Mint Radar: `owner()` cocok sama deployer asli 98/98, two-phase cocok 40/40 (cap/harga/per-wallet), timed cocok 16/17.

## Cara pakai di project gw
Checklist fitur buat dashboard/radar apapun: (1) siapa yang bikin dan track record-nya, (2) state yang bakal berubah (jadwal), (3) outcome setelahnya buat ngukur sinyal. Kalau launch project sendiri: sadar radar kayak gini bakal baca `owner()` dan getter jadwal kita.

## Caveat / jangan ditiru
- Contract bisa mindahin jadwal sendiri (FishingAi presale digeser ke window 1 detik yang udah lewat). Jadwal harus dibaca ulang tiap poll.
- Block serial deployer juga ngebuang mint populer (Kitsuneon 2.812 wallet). Trade-off.
- Site pihak ketiga: baca lewat GET publik aja, jangan load test.

## Bukti
- https://agenticmint.ai
- Map lengkap: catatan recon internal
