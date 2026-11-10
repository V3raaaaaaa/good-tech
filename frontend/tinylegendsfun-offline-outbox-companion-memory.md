---
name: Outbox offline-first buat memori companion AI
category: frontend
project: Tiny Legends (tinylegends.fun)
chain: -
tags: [offline-first, outbox, localstorage, zod, sync, ai-companion]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, public JS bundle of https://tiny-legends-production.up.railway.app/
---
# Outbox offline-first buat memori companion AI

## Ringkas
Momen latihan/ngobrol sama legend ("clubhouse memory") gak langsung di-POST terus dibuang kalo gagal. Tiap event masuk antrian di `localStorage` dengan key per owner + per legend, di-flush satu per satu ke server, dan dicoba lagi otomatis tiap browser `online` lagi.

## Kenapa bagus
- Koneksi HP putus-putus gak bikin memori companion hilang. Ini penting, karena "dia inget kita" itu inti produk companion.
- Antrian divalidasi schema pas dibaca ulang (`A.parse`, kemungkinan zod), jadi data localStorage yang korup/lama gak bikin crash.
- Ada batas keras 200 item. Kalo penuh, user dikasih tau terus terang ("Memory queue is full. Reconnect and retry...") daripada diem-diem buang data.
- Flush berurutan, ada lock (`m`), item dihapus cuma setelah server bales `ok`, terus hasilnya di-merge dedup by `id` dan di-sort `createdAt` (simpan 30 terbaru).
- Error baca/tulis storage ditangkep (mode private, kuota penuh) dan dikasih pesan jelas.

## Cara kerja
1. Key: `tiny-clubhouse-outbox:v1:<owner>:<legendId>` (ada versi `v1` biar bisa migrasi).
2. `start()`: load antrian → validasi → GET memori dari server → flush.
3. `record(e)`: push → simpan → flush.
4. `flush`: selama antrian ada isinya, POST item pertama, kalo ok hapus dan simpan, kalo gagal stop dan kasih pesan error.
5. `window.addEventListener("online", retry)`, plus `close()` pas unmount.
6. Fetch dibungkus `AbortSignal.timeout(10s)`.

## Cara pakai di project gw
- Event user apa pun yang gak boleh hilang (progress game, catatan, jawaban form) dan gak butuh konfirmasi sinkron.
- Kasih tiap event `id` dari client biar server bisa dedup (idempotent POST).
- Versi-in key storage-nya, validasi pake schema pas load, kasih cap, dan tampilin jumlah pending ke user.

## Caveat / jangan ditiru
- localStorage itu per-browser. Pindah device = antrian ketinggal, dan event itu gak pernah nyampe server.
- Kalo server gak dedup by id, retry setelah timeout bisa dobel.
- Jangan simpen data sensitif di outbox localStorage (gampang dibaca kalo ada XSS).

## Bukti
- Bundle publik: closure dengan `tiny-clubhouse-outbox:v1:${owner}:${legendId}`, endpoint `/api/v1/agents/${legendId}/clubhouse-memory`, cap `a.length>=200`, listener `"online"`.
