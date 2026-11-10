---
name: Ticket stateless (HMAC + AES-GCM) antar step multi-request
category: backend
project: forks.wiki
chain: -
tags: [serverless, hmac, aes-gcm, stateless, session, security]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, [netlify/lib/server.mjs](https://github.com/forkwiki/fork/blob/main/netlify/lib/server.mjs) + functions/launch.mjs
---

# Ticket stateless (HMAC + AES-GCM) antar step multi-request

## Ringkas
Flow 3 step (plan, build, submit) di serverless tanpa nyimpen state di DB atau memori: tiap step balikin "ticket" bertanda tangan HMAC yang berisi hasil step sebelumnya plus expiry. Data rahasia (mint secret key) dienkripsi di dalam ticket.

## Kenapa bagus
- Serverless function gak punya memori bareng antar instance; ticket ngebawa state-nya sendiri.
- Client gak bisa ngubah isi (HMAC-SHA256, dibandingin pakai `timingSafeEqual`), dan ticket punya TTL (plan 15 menit, send 150 detik).
- Secret tetap rahasia walau ticket ada di browser: AES-256-GCM dengan key turunan `sha256('forks-mint:' + SESSION_SECRET)`.
- Field `k` (`plan` / `send`) nyegah ticket satu step dipakai di step lain.

## Cara kerja
```js
seal(payload, ttl)  -> base64url(JSON{...payload, exp}) + '.' + hmac(body)
unseal(token)       -> cek hmac (timingSafeEqual) + exp, null kalau gagal
lock(buf)           -> iv(12) | tag(16) | aes-256-gcm(buf)   // di dalam payload
```
Step build: `seal({k:'send', mint, wallet, hashes, key: lock(mintSecret)}, 150)`. Step submit: `unseal`, terus `unlock`, cek hash tx, co-sign.

## Cara pakai di project gw
Buat flow apapun di Vercel/Netlify/Cloudflare yang butuh beberapa request berurutan (quote, build tx, submit; atau voucher mint), tanpa Redis. Bonus: sekalian jadi bukti server pernah nyetujuin langkah sebelumnya.

## Caveat / jangan ditiru
- Ticket bisa di-replay selama belum expired. Kalau aksinya harus sekali, tambahin nonce/ID yang dicatat di DB (forks pakai reserve repo di Supabase).
- Rotasi `SESSION_SECRET` = semua ticket dan session mati.
- Satu secret dipakai buat HMAC dan derive key enkripsi. Lebih bersih kalau pakai HKDF dengan label berbeda.

## Bukti
- [netlify/lib/server.mjs](https://github.com/forkwiki/fork/blob/main/netlify/lib/server.mjs) (`seal`/`unseal`), `netlify/functions/launch.mjs` (`lock`/`unlock`)
