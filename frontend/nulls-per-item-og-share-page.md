---
name: Share page per item + endpoint OG image server-side + export PNG di client
category: frontend
project: NULLS (nulls.world)
chain: -
tags: [opengraph, social-share, canvas, vercel, virality]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://nulls.world/card/001 + https://nulls.world/api/card-image?no=001&format=og
---
# Share page per item + endpoint OG image server-side + export PNG di client

## Ringkas
Tiap card yang terbit punya URL `/card/<no>`: HTML kecil (sekitar 2 KB) dengan `<title>`, `og:*` dan `twitter:card=summary_large_image` yang nunjuk ke `/api/card-image?no=<no>&format=og` (PNG 1200x630). Gambar full 1080x1500 dari endpoint yang sama tanpa `format`. Di client, tombol SAVE nge-render card yang sama di `<canvas>` lalu `toBlob` buat di-download. Tweet intent pakai URL share page, jadi preview di X langsung nampilin card-nya.

## Kenapa bagus
- Shell SPA-nya gak punya meta sama sekali, tapi share page yang ringan bikin tiap post user jadi kartu besar di timeline. Murah dan efektif buat viral loop.
- Cache CDN dipisah: HTML `max-age=60`, image `max-age=300`, jadi data baru cepat kelihatan dan render gambar tetap murah.
- Nomor yang gak ada balik ke halaman "NO SUCH CARD" yang ringan, bukan 500.
- Export di client gak butuh server: font di-preload pakai `document.fonts.load` sebelum draw, teks yang kepanjangan dikecilin pakai loop `measureText`, wordmark di-tint pakai `globalCompositeOperation='source-in'`.

## Cara kerja
- Route `/card/[no]` (serverless) → lookup DB → template HTML dengan meta OG.
- Route `/api/card-image?no&format=og|full` → render server-side (canvas/satori) → PNG + Cache-Control.
- Share: `x.com/intent/tweet?text=...&url=<origin>/card/<no>`.

## Cara pakai di project gw
- Buat hasil mint/claim/achievement: tiap token atau badge dapat share page sendiri dengan OG image, bukan cuma link ke homepage.
- Tambahin `format=og` (1200x630) terpisah dari gambar asli, karena rasio card gak cocok sama crop preview X.

## Caveat / jangan ditiru
- Nomor urut bisa dienumerasi: siapa pun bisa scrape `/card/1..N` dan dapat daftar handle X pemegang card plus total supply. Kalau itu sensitif, pakai slug acak.
- PNG full-nya 1.4 MB. Kompres atau pakai WebP buat yang gak dipakai preview.

## Bukti
- `curl -s https://nulls.world/card/001` → `og:image content="https://nulls.world/api/card-image?no=001&format=og"`, `twitter:card summary_large_image`, `cache-control: public, max-age=60`.
- `curl -sI "https://nulls.world/api/card-image?no=001"` → `image/png`, 1080x1500, `cache-control: public, max-age=300`. Varian `format=og` 326 KB.
