---
name: Proof-of-work kecil di browser sebelum bikin sesi
category: security
project: Breakout (breakoutprop.com)
chain: offchain
tags: [anti-bot, pow, login, rate-limit, session]
score: 6
status: verified
added: 2026-11-24
source: recon 2026-11-24, bundle publik portal.breakoutprop.com (assets/index-*.js), endpoint /api/internal/pow
---
# PoW login (double SHA-256, difficulty bit)

## Ringkas
Sebelum handshake sesi, client minta challenge `{data, difficulty, randomness}` dari server, lalu nyari nonce acak sampai `sha256(sha256(data ‖ nonce))` punya `difficulty` bit nol di depan. Solusinya ikut dikirim di request login.

## Kenapa bagus
- Biaya per percobaan login pindah ke penyerang tanpa CAPTCHA dan tanpa vendor.
- Difficulty diatur server per request, jadi bisa dinaikin buat IP/ASN yang berisik.
- Client lapor `{solution, duration, attempts}` → server dapat sinyal gratis soal jenis device.
- Pakai WebCrypto, gak nambah dependency.

## Cara kerja
```js
do {
  crypto.getRandomValues(nonce); buf.set(nonce, data.length)
  h = await sha256(await sha256(buf))
} while (new DataView(h).getUint32(0) >>> (32 - difficulty))
return { solution: hex(nonce), duration, attempts }
```
Challenge diambil dengan cookie sesi (tanpa sesi → 401), jadi challenge terikat ke sesi dan sekali pakai.

## Cara pakai di project gw
- Taruh di depan endpoint mahal: login, claim, voucher, mint permit.
- Challenge harus: terikat sesi/IP, kedaluwarsa cepat, sekali pakai, diverifikasi server dengan hash yang sama.
- Mulai dari 16–18 bit (puluhan ms di laptop), naikin adaptif.

## Caveat / jangan ditiru
- PoW SHA-256 murah banget buat GPU/ASIC. Ini rem, bukan tembok. Tetap butuh rate limit dan gate lain.
- Loop `await crypto.subtle.digest` per percobaan lambat di main thread. Buat difficulty tinggi pakai Worker.
- Nonce acak (bukan counter) bikin jumlah percobaan gak deterministik. Gak masalah, tapi jangan pakai `attempts` buat keputusan keamanan.

## Bukti
- Bundle: fungsi PoW dengan `crypto.subtle.digest("SHA-256", …)` dua kali dan `getUint32(0) >> 32 - difficulty`.
- Live: `GET https://iapi.breakoutprop.com/api/internal/pow` → 401 tanpa sesi.
