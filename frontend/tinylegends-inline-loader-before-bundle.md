---
name: Loading screen inline yang mirip game, digambar sebelum bundle 2.5 MB datang
category: frontend
project: Tiny Legends
chain: -
tags: [performance, perceived-speed, web-game, mobile, loading]
score: 5
status: verified
added: 2026-11-11
source: recon 2026-11-11, `play.tinylegendsgame.io.html` (snapshot recon)
---

# Loading screen inline yang mirip game, digambar sebelum bundle 2.5 MB datang

## Ringkas
HTML game cuma 5.8 KB. Isinya script inline kecil (3 KB) yang langsung gambar loading screen persis kayak punya game (slime lompat, warna, font), plus hint "putar HP" dalam bahasa pemain. Pas `game.js` 2.5 MB selesai dan jalan, loading screen game nerusin dari situ tanpa kedip.

## Kenapa bagus
- Di HP dengan sinyal jelek pemain langsung liat sesuatu yang hidup, bukan layar putih berdetik-detik. Bounce rate turun.
- Transisi mulus karena tampilannya sama persis ("Same co[lors]...").
- Hint landscape dilokalisasi dari `navigator.language` tanpa nunggu sistem i18n game.
- Gak butuh framework atau build tambahan.

## Cara kerja
```html
<canvas id="boot"></canvas>
<script>/* v1.0.407 drawn at once, before the game code arrives (2+ MB on a slow phone line) */
  // gambar background + slime animasi di requestAnimationFrame, stop pas window.AB.started
</script>
<script src="game.<hash>.js"></script>
```

## Cara pakai di project gw
Web game atau app berat: taruh "boot screen" inline <5 KB yang identik dengan loading screen asli, plus hint penting (orientasi, bahasa). Bundle di-hash biar bisa cache selamanya.

## Caveat / jangan ditiru
- Satu bundle 2.5 MB tetap lambat. Lebih baik dipecah (code split per mode) daripada cuma nutupin lamanya.
- Duplikasi gaya antara inline dan game harus dijaga manual.

## Bukti
- `play.tinylegendsgame.io.html` (snapshot recon): 2 script inline (`v1.0.203` rotate hint, `v1.0.407` boot screen), `game.b5d22526b6.js` 2,554,822 byte
