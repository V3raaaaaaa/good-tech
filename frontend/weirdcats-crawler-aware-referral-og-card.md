---
name: Link referral per-user dengan OG card yang dirender di browser lalu di-upload
category: frontend
project: Weird Cats
chain: -
tags: [og-image, referral, canvas, social-share, cache-busting, x-cards]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://weirdcats.xyz/r/nett0eth + https://weirdcats.xyz/weirdlist/printer/printer.js
---
# Link referral per-user dengan OG card yang dirender di browser lalu di-upload

## Ringkas
Tiap user dapet link `/r/<handle>`. Manusia yang buka langsung di-302 ke room (`?ref=<handle>`). Crawler (Twitterbot dkk) dapet HTML kecil berisi OG/Twitter card personal: judul "@handle printed Weirdlist ticket #1001" dan gambar `card.php?h=<handle>&v=<timestamp>`. Gambar kartunya dirender di browser user pakai Canvas, lalu di-upload ke server sebelum tombol "Share on X" aktif.

## Kenapa bagus
- Server gak perlu image rendering (gak ada headless Chrome / Satori / Sharp). Cocok buat shared hosting PHP.
- Tiap share punya preview unik dengan nama + PFP + nomor tiket, jadi CTR jauh lebih tinggi daripada OG generik.
- `?v=<timestamp>` bikin X gak nampilin card basi waktu user ganti avatar/kucing (X nge-cache card per URL).
- Tombol Share di-disable (`aria-disabled`) sampai upload kelar, jadi pas X crawl, gambar udah ada.

## Cara kerja
1. Frontend gambar kartu ke `<canvas>` (font pixel di-load dulu, nunggu `document.fonts` biar gak fallback), `toDataURL('image/png')`.
2. `POST api.php?a=card {png}` dengan header `x-weirdlist: 1`; server simpan PNG per user.
3. `/r/<handle>`: server cek User-Agent. Crawler -> HTML berisi `og:image = card.php?h=<handle>&v=<updated_at>`. Manusia -> 302 ke `/weirdlist/room-v2/?ref=<handle>`.
4. Teks share diambil acak dari 6 template, link referral ditaruh di dalam parameter `text` (bukan `url`) karena beberapa app X ngebuang parameter `url`.

## Cara pakai di project gw
- Buat leaderboard/referral/achievement card: render di client, upload PNG (batasi ukuran + cek magic bytes + re-encode di server), serve dari domain sendiri.
- Endpoint referral dua muka: UA crawler -> OG HTML, selain itu -> redirect. Taruh juga meta OG di HTML redirect-nya buat crawler yang gak ke-detect.
- Selalu pakai versi di URL gambar OG (`?v=updated_at`).

## Caveat / jangan ditiru
- Gambar dari client = user bisa upload gambar apa aja yang nanti di-serve dari domain lu sebagai preview. Server wajib validasi (dimensi, ukuran, re-encode, rate limit) dan siap takedown. Validasi server-side di project ini gak bisa dicek dari luar (unproven).
- UA sniffing bisa salah; X kadang crawl dengan UA lain.
- Rotasi template teks dipakai biar gak kebaca spam sama X; jangan sampai jadi alat spam massal.

## Bukti
- `curl -A Twitterbot https://weirdcats.xyz/r/nett0eth` -> 200 HTML dengan `og:image https://weirdcats.xyz/weirdlist/card.php?h=nett0eth&v=1794070548`; UA browser -> 302 ke `/weirdlist/room-v2/?ref=nett0eth`.
- `https://weirdcats.xyz/weirdlist/printer/printer.js` baris 433, 517-523 (`uploadCard`, Share nunggu upload).
- `https://weirdcats.xyz/weirdlist/printer/share.js` (6 template, link di dalam `text`).
- `https://weirdcats.xyz/weirdlist/shelter/shelter.js` baris 433-455 (pola sama buat adoption papers 1200x630).
