---
name: OAuth popup lewat BroadcastChannel + diagnosa per fase + fallback redirect di mobile
category: frontend
project: Blast (blast.fun)
chain: -
tags: [oauth, popup, broadcastchannel, ux, error-handling]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, public JS bundle https://www.blast.fun/ (Next.js chunk 00gc-ckp3omkc.js)
---
# OAuth popup lewat BroadcastChannel + diagnosa per fase + fallback redirect di mobile

## Ringkas
Login X/Google buka popup `about:blank`, set `opener = null`, lalu arahin ke `/mission-control/auth?provider&request=<uuid>`. Hasilnya dikirim balik lewat `BroadcastChannel("…oauth:<uuid>")`, bukan `window.opener.postMessage`. Selagi nunggu, parent nge-poll popup tiap 400 ms buat tahu popup lagi di fase mana. Error-nya jadi spesifik, dan di mobile otomatis pindah ke full redirect.

## Kenapa bagus
- `opener = null` motong akses provider/halaman pihak ketiga ke window lu (reverse tabnabbing), tapi komunikasi tetap jalan lewat BroadcastChannel same-origin.
- Request ID random per percobaan. Pesan cuma diterima kalau `requestId` + `provider` + `status` cocok, plus panjang token dibatasi (1–2048).
- Ada handshake `acknowledged`: popup baru nutup sendiri setelah parent konfirmasi terima.
- Diagnosa fase: popup bisa dibaca (masih di domain sendiri) = "bootstrap"; cross-origin = lagi di provider; balik bisa dibaca = "callback". Kalau ditutup, user dapet pesan yang bener ("provider nggak balik", "callback ketutup sebelum verifikasi", "timeout 300s"), dan detail teknisnya ada buat support.
- Query `code/state/token` di URL di-redact sebelum masuk log error.
- iOS/Android (termasuk iPad yang ngaku Macintosh, dicek lewat `maxTouchPoints`) pakai redirect + `return=` dengan whitelist tujuan.

## Cara kerja
- `openPopup()` → `new BroadcastChannel(key)` → `setInterval(400)` cek `popup.closed` / try-catch `popup.location.href` → `setTimeout(300000)`.
- Halaman callback: `postMessage({requestId, provider, status, accessToken?})` ke channel, tunggu `acknowledged`, terus `window.close()`.
- Error ditampilin per kode (`OAUTH_FAILED`, `POPUP CLOSED AFTER Ns // LAST PHASE …`).

## Cara pakai di project gw
- Semua app yang pakai OAuth popup (X, Discord, Google) atau login wallet yang butuh popup. Pola ini juga cocok buat flow "connect X buat verifikasi follow".

## Caveat / jangan ditiru
- Kode frontend blast.fun itu proprietary (bundle publik, bukan repo open source; kontraknya BUSL-1.1). Yang ditiru polanya, bukan kodenya.
- BroadcastChannel nggak jalan lintas origin atau lintas profil browser, jadi callback harus same-origin.
- Polling `location` itu best-effort. Fase "cross-origin" cuma tebakan.
- Dibaca dari bundle minified.

## Bukti
- `https://www.blast.fun/_next/static/immutable/chunks/00gc-ckp3omkc.js` module 892288 (fungsi `R`: `window.open("about:blank", …)`, `h.opener = null`, `BroadcastChannel`, interval 400, timeout 3e5) dan module 43344 (deteksi mobile + redirect dengan whitelist `["onboarding","restore","owner"]`)
