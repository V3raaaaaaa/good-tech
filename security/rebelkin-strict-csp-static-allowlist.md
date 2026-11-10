---
name: CSP ketat + header lengkap buat halaman allowlist statis
category: security
project: RebelKin
chain: -
tags: [csp, security-headers, vercel, turnstile, clickjacking]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, response headers https://rebelkin.xyz/ dan https://rebelkin.xyz/api/config
---
# CSP ketat + header lengkap buat halaman allowlist statis

## Ringkas
Situs allowlist kecil (vanilla JS, tanpa framework) yang ngirim CSP super sempit: script cuma dari origin sendiri + Cloudflare Turnstile, `form-action` dikunci ke origin sendiri + x.com, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'self'`, tanpa `unsafe-inline` sama sekali.

## Kenapa bagus
- Situs WL itu target favorit buat drainer injection / phishing clone. Kalau ada XSS atau script pihak ketiga ketitipan, CSP ini bikin script asing nggak bisa jalan dan nggak bisa exfil ke domain lain (`connect-src 'self' challenges.cloudflare.com`).
- `style-src 'self'` tanpa inline: style juga nggak bisa diinject.
- `frame-ancestors 'none'` + `X-Frame-Options: DENY`: nggak bisa di-iframe buat clickjacking.
- API pakai `cache-control: no-store` + `referrer-policy: no-referrer`, halaman statis pakai `strict-origin-when-cross-origin`.

## Cara kerja
Header yang dikirim (semua response):
```
content-security-policy: default-src 'self'; script-src 'self' https://challenges.cloudflare.com;
  frame-src https://challenges.cloudflare.com; connect-src 'self' https://challenges.cloudflare.com;
  img-src 'self' data:; style-src 'self'; object-src 'none'; base-uri 'self';
  frame-ancestors 'none'; form-action 'self' https://x.com
strict-transport-security: max-age=63072000
x-content-type-options: nosniff
x-frame-options: DENY
permissions-policy: camera=(), microphone=(), geolocation=()
```
Supaya bisa tanpa `unsafe-inline`, semua JS di file eksternal (`/app.js` sebagai ES module), callback Turnstile dipasang lewat `window.onTurnstileLoad` dan script Turnstile di-append dinamis dari file itu juga, bukan `<script>` inline.

## Cara pakai di project gw
- Di Vercel taruh di `vercel.json` `headers` untuk `/(.*)`; di Next.js pakai `headers()` di `next.config`.
- Mulai dari `default-src 'self'`, lalu whitelist cuma domain yang beneran dipakai (captcha, RPC, WalletConnect relay kalau ada dApp).
- Pindahin semua inline script/style ke file. Kalau framework maksa inline, pakai nonce, jangan `unsafe-inline`.

## Caveat / jangan ditiru
- Ini gampang karena situsnya nggak ada wallet connect. dApp beneran perlu `connect-src` ke RPC/relay dan sering `wss:`; tetap bisa ketat tapi daftarnya lebih panjang.
- `access-control-allow-origin: *` di aset statis mereka nggak masalah, tapi jangan ikut nyalain itu di API yang pakai cookie.
- HSTS tanpa `includeSubDomains`/`preload`; kalau mau lebih keras, tambahin.

## Bukti
- `curl -sI https://rebelkin.xyz/` dan `curl -sI https://rebelkin.xyz/api/config` (diambil 2026-11-11).
- https://rebelkin.xyz/app.js: Turnstile di-load lewat `document.createElement('script')`, nggak ada inline script di HTML.
