---
name: CSRF guard murah pakai custom request header + tanpa CORS
category: security
project: Weird Cats
chain: -
tags: [csrf, cors, preflight, php, cookie-session]
score: 5
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://weirdcats.xyz/weirdlist/printer/printer.js + https://weirdcats.xyz/weirdlist/shelter/shelter.js
---
# CSRF guard murah pakai custom request header + tanpa CORS

## Ringkas
Semua request yang ngubah state (`print`, `adopt`, `card`) dikirim dengan header `x-weirdlist: 1` dan `content-type: application/json`. Server gak ngirim header CORS apa pun, dan `OPTIONS` preflight dari origin lain dijawab 404. Hasilnya: situs lain gak bisa nembak POST atas nama user yang lagi login, walau session-nya cookie.

## Kenapa bagus
- Gak perlu token CSRF di form/HTML, cocok buat SPA statis + PHP.
- Browser wajib preflight buat header custom dan JSON content-type; preflight gagal = request gak pernah dikirim.
- Lapis kedua di atas cookie `SameSite=Lax`.

## Cara kerja
```js
fetch(`${API}?a=${action}`, {
  method: 'POST', credentials: 'same-origin',
  headers: { 'content-type': 'application/json', 'x-weirdlist': '1' },
  body: JSON.stringify(body),
});
```
Server: tolak POST kalau header `x-weirdlist` gak ada atau `content-type` bukan `application/json`; jangan pernah set `Access-Control-Allow-Origin` / `Allow-Headers`.

## Cara pakai di project gw
- Pasang di semua endpoint mutasi yang pakai cookie session.
- Cek header di server (bukan cuma ngandelin browser), dan tolak `text/plain` / form-encoded.
- Kalau nanti butuh CORS buat origin lain, allowlist origin spesifik, jangan `*` plus credentials.

## Caveat / jangan ditiru
- Ini bukan auth. Gak ngelindungin dari XSS di origin sendiri, dan gak ngaruh ke bot yang manggil API langsung.
- Gw cuma bisa buktiin sisi browser (preflight 404, gak ada CORS header). Apakah server beneran nolak POST tanpa header itu gak dites (sengaja, gak boleh POST). Statusnya verified buat desain client + respon preflight.
- Endpoint GET jangan sampai ngubah state; di project ini `a=x_login` (GET) bikin state OAuth, itu wajar.

## Bukti
- `https://weirdcats.xyz/weirdlist/printer/printer.js` baris 44-50, `https://weirdcats.xyz/weirdlist/shelter/shelter.js` baris 22-28.
- `OPTIONS https://weirdcats.xyz/weirdlist/api.php?a=print` dengan `Origin: https://evil.example` dan `Access-Control-Request-Headers: x-weirdlist,content-type` -> HTTP 404, tanpa header `access-control-*`.
- `GET .../api.php?a=me` dengan Origin asing -> 200 tanpa `Access-Control-Allow-Origin` (browser lain gak bisa baca).
