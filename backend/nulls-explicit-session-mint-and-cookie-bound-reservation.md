---
name: Session cookie cuma dibuat on-demand + reservasi kode terikat cookie sampai di-claim
category: backend
project: NULLS (nulls.world)
chain: -
tags: [sessions, idempotency, race-conditions, invite-codes, vercel]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://nulls.world/ (inline app script, publik) + https://nulls.world/api/me
---
# Session cookie cuma dibuat on-demand + reservasi kode terikat cookie sampai di-claim

## Ringkas
`GET /api/me` biasa gak pernah bikin cookie. Cookie session (`sid`, HttpOnly, 1 tahun) cuma di-mint lewat `GET /api/me?session=1`, dan server ngasih tahu lewat header `X-Nulls-Session: 1` bahwa browser sekarang punya cookie. Check kode invite baru dikirim setelah itu. Kode yang diterima di-*reserve* ke cookie itu (bukan langsung di-claim), dan baru jadi milik permanen setelah login X selesai.

## Kenapa bagus
- Nutup race klasik: dua tab sama-sama load, response telat dari tab lain nge-set cookie baru, terus kode yang tadinya ke-reserve nyangkut di cookie yang udah gak dipegang browser. Karena cuma satu jalur yang boleh mint cookie, masalah ini gak bisa terjadi.
- Retry aman (idempotent): kode yang sama dari cookie yang sama di-reserve ulang ke pemilik yang sama, jadi client boleh auto-retry sekali kalau jaringan putus.
- Gak ada cookie buat pengunjung pasif. Crawler gak nyampah row session di DB.
- Kode gak pernah dikirim ke client. Validasinya server-side dengan normalisasi (accent dibuang, uppercase, A-Z0-9 aja), jadi "two words" atau "two-words" sama-sama lolos.

## Cara kerja
1. Load page: `GET /api/me` → `{"access":"none"}` atau status card, tanpa Set-Cookie.
2. User submit kode. Kalau belum punya sid: `GET /api/me?session=1` → Set-Cookie + `X-Nulls-Session: 1`.
3. `POST /api/code {code}` → server normalisasi, cek, lalu reserve ke sid (`ok`), atau balas `wrong/busy/not_ready`.
4. Login X → callback mengikat kode yang di-reserve ke akun X dan nerbitin card bernomor urut.

## Cara pakai di project gw
- Buat flow invite/WL code/claim: pisahin "reserve" dan "claim". Reserve boleh diulang, claim cuma sekali dan butuh identitas kuat (OAuth/signature).
- Expose header kecil (`X-App-Session: 1`) biar SPA tahu status cookie tanpa harus bisa baca cookie HttpOnly.
- Normalisasi input dengan fungsi yang sama persis di client (buat tampilan) dan server (buat keputusan).

## Caveat / jangan ditiru
- Reservasi butuh TTL/expiry di server. Kalau gak ada, kode bisa disandera cookie yang ditinggal (di sini TTL-nya gak kelihatan dari luar, unproven).
- Rate limit wajib di endpoint check kode (client menangani 429, jadi limit di server kemungkinan ada).
- Implementasi server-nya proprietary. Yang layak ditiru polanya.

## Bukti
- `curl -sI https://nulls.world/api/me` → tanpa set-cookie. `curl -sI "https://nulls.world/api/me?session=1"` → `set-cookie: nulls_sid=...; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax` + `x-nulls-session: 1`.
- Komentar di script inline https://nulls.world/ : "Only start (the check's own ask, /api/me?session=1) makes a new browser's cookie; the load's plain ask never does" dan "the server reserves the same code to the same browser again ... nothing is claimed before X sign-in".
