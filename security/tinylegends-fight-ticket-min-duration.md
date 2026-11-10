---
name: Tiket fight dari server + durasi minimum sebelum hasil diterima (anti-cheat ringan)
category: security
project: Tiny Legends
chain: -
tags: [anti-cheat, game, p2e, rate-limit, server-ticket]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) (fightStart/ticket/report)
---

# Tiket fight dari server + durasi minimum sebelum hasil diterima

## Ringkas
Pas fight mulai, client minta tiket ke server (`/earn/ticket {kind}` → `{id}`, server nyatet waktunya). Hasil fight (`/earn/raid`, `/earn/battle`) wajib bawa id tiket, dan client nunggu sampai durasi minimum per mode lewat (`FIGHT_MIN[kind]` + 1.5 s), plus jeda antar laporan (raid 16 s, battle 11 s). Server bisa nolak hasil yang datang lebih cepat dari yang mungkin.

## Kenapa bagus
- Murah: gak perlu simulasi battle di server. Speed hack dan script "submit 1000 win per detik" langsung mentok.
- Tiket sekali pakai per fight = gak bisa replay satu hasil berkali-kali.
- Antrian per mode (`sendQ[kind]`) di client sama dengan aturan server, jadi pemain jujur gak pernah kena tolak.
- Digabung sama cap harian poin, total yang bisa dicuri per akun per hari punya batas atas yang jelas.

## Cara kerja
```js
fightStart(kind): tk[kind] = POST /earn/ticket {kind} -> {id}; tkAt[kind] = now
report(kind, path, body):
  wait until max(t0, ticket.at) + FIGHT_MIN[kind]*1000 + 1500  and  lastSent[kind] + gap
  POST path {...body, ticket: id}          // server: ticket ada, belum dipakai, umur >= FIGHT_MIN
```

## Cara pakai di project gw
Lapis pertama buat game web apapun yang hasilnya dapet reward (mini game skyshot, quest game): tiket server + durasi minimum + cap harian. Kalau reward-nya bernilai, tambahin lapis kedua: seed RNG dari server + replay input di server (deterministic lockstep) atau cek statistik (win rate, waktu vs power).

## Caveat / jangan ditiru
- **Ini bukan server-authoritative.** Isi hasilnya (`win`, `allAlive`, `secs`, `stars`) tetap dari client. Bot yang sabar nunggu durasi minimum tetap bisa lapor "menang 3 bintang" tiap fight. Yang dibatasi cuma kecepatan, bukan kejujuran.
- Durasi minimum yang dipatok di client (`FIGHT_MIN`) bisa dibaca bot, jadi bot tahu persis harus nunggu berapa lama.
- Leaderboard Tiny Legends masih nunjukin angka clamp (guildDamage = 1e12) di top player. Statistik non-reward gak dijaga sama sekali.

## Bukti
- `game.js` (snapshot recon): `fightStart`, `ticket`, `report` (gap raid 16e3 / battle 11e3, min = FIGHT_MIN + 1500), `/earn/ticket`
