---
name: Share card publik yang dipisah dari data privat + SVG->PNG di browser
category: frontend
project: RebelKin
chain: -
tags: [share-card, privacy, svg, canvas, og-image, virality]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://rebelkin.xyz/app.js, https://rebelkin.xyz/privacy, https://rebelkin.xyz/terms
---
# Share card publik yang dipisah dari data privat

## Ringkas
Abis apply, user dapet link `/card/<share_id>` yang nampilin handle + receipt aplikasi aja. Gambar card di-render server sebagai SVG (`?format=svg`), dan tombol download ngubahnya jadi PNG 1200x630 di browser lewat `<canvas>`, tanpa server image renderer.

## Kenapa bagus
- Viral loop WL ("I found my kin") tanpa bocorin wallet: share ID terpisah dari ID aplikasi, dan card eksplisit nggak nampilin wallet, bukti sosial, keputusan, atau catatan reviewer.
- Copy-nya jujur: card "bukan approval atau mint pass", jadi nggak ada orang jualan "WL card".
- SVG -> PNG di client: server cuma generate SVG teks (murah), ukuran 1200x630 pas buat OG/X card.
- Tombol share pakai X intent URL, nggak butuh scope `tweet.write`.

## Cara kerja
```js
share = location.origin + '/card/' + a.share_id;
$('card-image').src = share + '?format=svg';
// download
const img = new Image(); img.src = share + '?format=svg'; await img.decode();
const c = document.createElement('canvas'); c.width = 1200; c.height = 630;
c.getContext('2d').drawImage(img, 0, 0);
const blob = await new Promise(r => c.toBlob(r, 'image/png'));
```
Share ke X: `https://x.com/intent/tweet?text=...&url=<share>`; halaman `/card/<id>` kasih meta OG supaya X nampilin preview.

## Cara pakai di project gw
- Bikin kolom `share_id` random (bukan auto-increment, bukan wallet) di tabel aplikasi/claim.
- Endpoint card cuma baca field yang memang publik; whitelist field, jangan `SELECT *`.
- Kalau SVG-nya embed font/gambar, inline sebagai data URI supaya canvas nggak tainted dan render konsisten.

## Caveat / jangan ditiru
- `drawImage` SVG yang nge-load resource eksternal bisa gagal/tainted; mereka aman karena same-origin.
- Kalau `share_id` pendek/berurutan, card bisa di-enumerate. Pakai minimal 96-bit random. Panjang share_id mereka: unproven (nggak dicek).
- Teks handle di SVG wajib di-escape server-side (XML injection). Implementasi server mereka belum dilihat.

## Bukti
- https://rebelkin.xyz/app.js fungsi `receipt()` dan handler `download-card`.
- https://rebelkin.xyz/privacy ("Cards do not expose wallet addresses, social evidence, decisions, or private notes").
- https://rebelkin.xyz/terms bagian "Sharing".
