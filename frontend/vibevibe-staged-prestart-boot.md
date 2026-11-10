---
name: Boot SPA bertahap: inline script prefetch data pertama + modulepreload dari manifest build
category: frontend
project: vibe/vibe (Seedify)
chain: -
tags: [performance, lcp, vite, modulepreload, prefetch, spa]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `testnet.vibevibe.fun.html` (snapshot recon)
---

# Boot SPA bertahap: inline script prefetch data pertama + modulepreload dari manifest build

## Ringkas
Script kecil inline di `<head>` jalan sebelum bundle React. Script itu langsung (1) kasih hint download file JS per tahap sesuai route, dan (2) "parkir" fetch API pertama yang bakal dibutuhin halaman (misal data chart token), biar network gak nunggu React selesai evaluasi.

## Kenapa bagus
- Hasil terukur di komentar kode mereka: chart token (LCP) di HP throttle 4x / slow 4G turun dari 8.4 s + 2.5 s, karena fetch-nya jalan barengan dengan evaluasi JS.
- Manifest route → chunk digenerate build (Vite) dan ditaruh di `<meta name="seedify-landing">`, jadi gak ada daftar file manual.
- Hint bertahap (shell → runtime → route), tiap tahap nunggu tahap sebelumnya, jadi gak rebutan bandwidth sama file kritis.
- Fetch yang diparkir diambil app sekali (`candlesPrestart.ts`) dengan batas umur, dan ada test yang jaga URL-nya sama dengan yang dipakai client.
- Pengunjung pertama (belum setuju terms) gak di-prefetch apa-apa, jadi gak buang data.
- Font dipecah: `core` (ASCII yang dipakai UI) di-preload 5.3 kB, `ext` cuma diambil pas ada karakternya (`unicode-range`).

## Cara kerja
```html
<meta name="seedify-landing" content='{"app":[...],"runtime":[...],"routes":{"/":[...],"token":[...]}}'>
<script data-live-config-prestart="live">
  // baca manifest -> <link rel=modulepreload> per tahap
  // kalau route /token/:addr dan user udah accept -> fetch('/api/.../candles?...') simpan di window.__prestart
</script>
<script type="module" src="/static-v2/index-*.js"></script>
```

## Cara pakai di project gw
Buat dashboard/radar/token page yang LCP-nya data (chart, tabel): inline prestart buat fetch pertama + simpan promise-nya di `window`, terus app pakai kalau umurnya masih segar. Generate manifest route→chunk dari build, jangan manual.

## Caveat / jangan ditiru
- Logika duplikat antara inline script dan app. Harus dijaga pakai test biar URL/param-nya gak beda.
- Nambah kompleksitas yang besar. Buat app kecil, `modulepreload` bawaan Vite udah cukup.
- CSP harus izinin inline script (atau pakai hash/nonce).

## Bukti
- `testnet.vibevibe.fun.html` (snapshot recon): meta `seedify-boot-shell` + `seedify-landing`, inline script `data-live-config-prestart`, komentar pengukuran 8.4 s / 2.5 s dan font 15.3 kB → 5.3 kB
