---
name: Status checkout + headroom per user dari server (kill-switch per metode bayar)
category: backend
project: Breakout (breakoutprop.com)
chain: offchain
tags: [checkout, kill-switch, payments, cap, api-design]
score: 6
status: verified
added: 2026-11-24
source: recon 2026-11-24, https://btg-prod-api.breakoutprop.com/checkout/status , /checkout/headroom , /users/products (GET publik, perlu browser asli karena Cloudflare)
---
# Checkout status + headroom dari server

## Ringkas
Frontend gak pernah nebak apakah user boleh beli. Dua endpoint baca kecil yang nentuin: `checkout/status` (metode bayar mana yang hidup, plus alasan kalau mati) dan `checkout/headroom` (berapa sisa kuota modal user terhadap cap total).

## Kenapa bagus
- Matiin satu processor (kartu / PayPal / crypto) cukup dari server, tanpa deploy frontend.
- Field `reason` per metode bikin UI bisa jelasin kenapa, bukan cuma tombol abu-abu.
- Cap total ($200K modal aktif per orang) dihitung server; cart cuma nampilin sisa.
- Katalog produk (`/users/products`) juga satu sumber: harga, target, limit, add-on dengan `markup` persen.

## Cara kerja
```
GET /checkout/status   → {"available":true,"methods":{"card":{"available":true,"reason":null},"paypal":{…},"confirmo":{…}},"checkoutDisabled":false}
GET /checkout/headroom → {"active_capital":0,"cap":200000,"headroom":200000}
GET /users/products    → [{name,type,size,cost,goals,maxDailyLoss,maxDrawdown,attributes:[{name,markup}]}]
```
Alur bayar: `checkout/validate` → `checkout/session` (atau `paypal-session` / `confirmo-session` / `balance-session`) → `checkout/finalize`. Saldo payout bisa dipakai bayar sebagian.

## Cara pakai di project gw
- Mint/sale page: endpoint `status` dengan flag per jalur (public, WL, kartu, crypto) + `reason`.
- Endpoint `headroom` buat cap per wallet/akun, dihitung server, divalidasi ulang di `validate`.
- Add-on sebagai `markup` persen di katalog, bukan harga hardcode di frontend.

## Caveat / jangan ditiru
- Katalog masih ngirim add-on yang disembunyiin UI ("Breach Insurance", markup 10) dan frontend yang nge-filter. Kalau sesuatu belum dijual, jangan dikirim.
- `headroom` tanpa login balikin cap penuh. Aman karena cuma baca, tapi validasi beneran wajib di server saat bayar.

## Bukti
- Respons live 2026-11-24 seperti di atas (17 produk, 3 metode bayar).
- Bundle: konstanta `checkout/status`, `checkout/headroom`, `checkout/validate`, `checkout/finalize`.
