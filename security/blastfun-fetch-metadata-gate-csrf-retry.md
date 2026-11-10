---
name: Gate cookie Fetch-Metadata + CSRF double-submit __Host- + fetch wrapper yang retry sendiri
category: security
project: Blast (blast.fun)
chain: -
tags: [csrf, fetch-metadata, cookies, nextjs, api-gateway, retry]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://www.blast.fun/ response headers dan public JS bundle
---
# Gate cookie Fetch-Metadata + CSRF double-submit __Host- + fetch wrapper yang retry sendiri

## Ringkas
Semua `/api/*` butuh cookie `__Host-blast_gate` (HttpOnly, Secure, SameSite=Lax, 2 jam, isinya token bertanda tangan). Cookie itu cuma diterbitin `/api/gate` kalau request-nya bawa `Sec-Fetch-Site: same-origin`. Request yang ngubah state juga harus bawa header `x-blast-csrf` yang nilainya sama dengan cookie `__Host-blast_csrf`. Di client, `globalThis.fetch` dibungkus: kalau dapet `401` dengan `x-blast-gate: required`, dia refresh gate sekali (promise di-dedupe) terus ngulang request aslinya.

## Kenapa bagus
- Prefix `__Host-` maksa Secure + Path=/ + tanpa Domain, jadi subdomain lain nggak bisa nimpa cookie.
- Fetch Metadata itu murah (tanpa JS challenge) dan langsung nolak request cross-site dari browser (CSRF, embed, hotlink API dari web lain).
- Wrapper-nya rapi: cuma buat path `/api` same-origin (yang `//host` ditolak), `credentials: 'omit'` dipaksa jadi `same-origin`, body `ReadableStream` nggak di-retry, `Request` di-clone sebelum dikirim, ngehormatin `AbortSignal`, dan ditandai `Symbol.for` biar nggak dobel bungkus.
- Retry 503/network cuma buat request yang idempotent, maks 2 kali, `Retry-After` di-cap 15 detik + jitter, dan UI nampilin status "busy — retrying".
- Ditambah CSP nonce + `strict-dynamic`, `frame-ancestors 'none'`, HSTS 2 tahun.

## Cara kerja
- `GET /api/gate`: tanpa `Sec-Fetch-Site: same-origin` → `403 gate_forbidden`; dengan header itu → `204` + `Set-Cookie: __Host-blast_gate=v1.<exp>.<nonce>.<mac>`.
- Endpoint lain tanpa cookie → `401 {"code":"gate_required"}` + header `x-blast-gate: required`.
- Client: `installGate()` ganti `window.fetch`. Header CSRF diambil dari `document.cookie` dan disisipin di tiap POST.

## Cara pakai di project gw
- App Next.js/Vercel yang API-nya cuma buat frontend sendiri: middleware cek `Sec-Fetch-Site`/`Origin` + cookie HMAC berumur pendek, plus wrapper fetch kayak gini biar user nggak pernah lihat error kalau cookie kadaluarsa.

## Caveat / jangan ditiru
- Kode frontend blast.fun itu proprietary (bundle publik, bukan repo open source; kontraknya BUSL-1.1). Yang ditiru polanya, bukan kodenya.
- **Ini bukan anti-bot.** Header `Sec-Fetch-*` gampang dipalsuin dari curl/script: `curl -H 'Sec-Fetch-Site: same-origin' https://www.blast.fun/api/gate` → 204 + cookie (dites 2026-11-11). Proteksinya buat browser (CSRF/cross-site), bukan buat Sybil/scraper. Buat itu tetap butuh rate limit + Turnstile (CSP-nya juga ngizinin `challenges.cloudflare.com`).
- Kalau token gate nggak diikat ke apa pun (IP/UA/sesi), dia cuma "proof of same-origin", jangan dianggap lebih dari itu.

## Bukti
- Response header https://www.blast.fun/ (CSP, `set-cookie: __Host-blast_gate…; Max-Age=7200; HttpOnly; Secure; SameSite=Lax`)
- `https://www.blast.fun/_next/static/immutable/chunks/25_3i4_uf0sdk.js` module 303693 (wrapper `/api/gate`, `Symbol.for("blast.apiGate.fetch")`)
- `00gc-ckp3omkc.js` module 115067/121917 (`__Host-blast_csrf` → header `x-blast-csrf`)
- `3gqb3dw7d-dar.js` (retry: hanya 503/network, idempotent, maks 2, `Retry-After` ≤ 15 s + jitter)
