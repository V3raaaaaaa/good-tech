---
name: Harga launch window terbatas + progress offline dengan cap dan efisiensi
category: tokenomics
project: Tiny Legends
chain: -
tags: [game-design, idle, launch-pricing, retention, fomo]
score: 5
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) (AB.LAUNCH, CONFIG.OFFLINE_*)
---

# Harga launch window terbatas + progress offline dengan cap dan efisiensi

## Ringkas
Dua desain kecil yang ngatur ritme pemain:
1. **Launch window 7 hari:** rank/Mint Level diskon 30%, dan pack naik jadi Nx harga setelah window lewat. Ada countdown di UI ("Buy at launch price now!").
2. **Progress offline:** pas tab ditutup, party tetap "berjuang", tapi dihitung maksimal 12 jam dengan efisiensi 75%, plus storage passive 8 jam yang bisa ditambah pakai item (Big Satchel).

## Kenapa bagus
- Launch window ngumpulin pemasukan di awal (yang ngisi reward pool) dengan aturan yang jelas dan ada batas waktunya, bukan diskon acak.
- Offline cap 12 jam dengan efisiensi 75% = pemain dihargai karena balik lagi tiap ~12 jam (retensi), tapi main aktif tetap lebih untung. Storage passive yang bisa di-upgrade jadi sink yang wajar.
- Waktu launch diambil dari config (`LAUNCH_AT`) atau server (`setSrv`), jadi countdown konsisten di semua client.

## Cara kerja
```js
AB.LAUNCH = {DAYS: 7, RANK_OFF: .3}
rankPrice(c) = launchActive ? c * (1 - RANK_OFF) : c
CONFIG: OFFLINE_CAP_H: 12, OFFLINE_MAX_H: 12, OFFLINE_EFFICIENCY: .75; EARN.STORE_H: 8; SATCHEL: {hours: 8, days: 7, USD: .75}
offlineGain = rate * min(elapsedH, OFFLINE_CAP_H) * OFFLINE_EFFICIENCY
```

## Cara pakai di project gw
Game idle/clicker atau app dengan reward harian: cap offline + efisiensi < 1, dan window harga launch yang jelas batas waktunya. Tampilin countdown dari waktu server.

## Caveat / jangan ditiru
- Diskon launch + "harga naik Nx nanti" = FOMO. Di P2E ini dorong orang beli di puncak hype. Tiny Legends: token −93% dalam 2 hari launch window.
- Perhitungan offline di client (pakai `Date.now()`) bisa dicurangi dengan ganti jam device kalau server gak nyimpen `lastSeen` sendiri.

## Bukti
- `game.js` (snapshot recon): `AB.LAUNCH={DAYS:7,RANK_OFF:.3}`, `AB.Launch.rankPrice`, `OFFLINE_CAP_H:12`, `OFFLINE_EFFICIENCY:.75`, string "Every pack costs {0}x after the launch window"
