---
name: Cloud save offline-first dengan merge berdasarkan progress + optimistic concurrency (409 stale)
category: backend
project: Tiny Legends
chain: -
tags: [game, save-sync, offline-first, concurrency, siwe]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) (cloudPull/cloudPush)
---

# Cloud save offline-first dengan merge berdasarkan progress + optimistic concurrency

## Ringkas
Game jalan penuh offline (save di localStorage). Kalau login wallet, save di-push ke server tiap ~60 detik. Konflik antar device diselesaikan pakai *progress* (wave tertinggi, lalu total level hero), bukan "yang terakhir nulis menang". Server pakai `base` timestamp: push dengan base lama ditolak `409 stale`, client tarik versi server dan ambil yang progress-nya lebih jauh.

## Kenapa bagus
- Pemain gak pernah kehilangan progress gara-gara device lama nimpa device baru. "Yang lebih jauh menang" itu aturan yang dipahami pemain.
- Optimistic concurrency (`base` = `at` terakhir dari server) tanpa lock dan tanpa WebSocket.
- Login wallet (personal_sign nonce dari server, isi pesan mirip SIWE: URI, Chain ID, Nonce, Issued At) → session bearer, dan session diputus kalau wallet ganti akun di tengah sign-in.
- Toast "Newer progress from your other device loaded" bikin pemain ngerti apa yang terjadi.
- Bisa main tanpa wallet dulu, dan earn baru nyala setelah bayar. Onboarding gampang.

## Cara kerja
```js
cloudPush: POST /save {address, at, version, save, power, base}
  409 {error:"stale"} -> GET /save; if prog(server) > prog(local) replace(local) else push lagi dengan base baru
cloudPull: GET /save; cmp = waveServer - waveLocal || levelsServer - levelsLocal
  if cmp > 0 || (cmp == 0 && server.at > local.lastSeen + 5s) -> replace(local)
signIn: GET /auth/nonce?address -> personal_sign(msg) -> POST /auth/login -> {session, exp}
```

## Cara pakai di project gw
Buat web game atau app apapun yang offline-first: pakai metrik progress yang monoton buat resolve konflik, `base` timestamp buat optimistic concurrency, dan login wallet yang nonce-nya dari server.

## Caveat / jangan ditiru
- **Ini cuma aman buat game TANPA uang.** Di Tiny Legends save dari client (gems, hero, wave) masuk ke server, dan hasil battle dilaporin client terus jadi poin token. Kalau ada reward bernilai, state yang ngehasilin reward harus dihitung server (atau minimal di-replay/diverifikasi).
- Merge "progress lebih jauh menang" bisa nimpa item/beli-an yang cuma ada di save "kalah". Item dari pembelian harus disimpan server terpisah (mereka pakai `/earn/state` + `packGift`).
- Fallback nonce `Math.random()` di client kalau `/auth/nonce` gagal = replay sign-in. Server harus wajibin nonce sendiri.

## Bukti
- `game.js` (snapshot recon): fungsi `signIn1`, `cloudPull`, `cloudPush`, `api()`
