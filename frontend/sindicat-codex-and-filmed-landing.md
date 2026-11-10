---
name: Codex aturan dengan angka asli game + landing pakai klip gameplay hover-to-play
category: frontend
project: SINDICAT
chain: -
tags: [docs, transparency, landing-page, onboarding, trust]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `sindicat.game_codex.html.html` (snapshot recon) + sindicat.game.html
---

# Codex aturan dengan angka asli game + landing pakai klip gameplay hover-to-play

## Ringkas
1. **Codex:** satu halaman statis yang nulis tiap aturan game **dengan angka yang dipakai game sekarang** (harga jual per strain, waktu matang, bail, fee market 1%, durability, ukuran hideout, key binding). Motonya: "the codex follows the code. When a number changes in the game, it changes here." Plus "No spoilers, no promises: what a cat can go and check."
2. **Landing:** loop game dijelasin 5 kartu (Gather, Craft, Produce, Sell, Stay clean), tiap kartu video pendek **direkam dari game asli** yang muter pas di-hover. Gak ada render konsep.

## Kenapa bagus
- Di dunia web3 yang penuh janji, halaman yang cuma isinya fakta yang bisa dicek itu sinyal trust yang kuat.
- Pemain bisa ngitung sendiri (berapa SIN/jam per trade), dan farmer serius suka. Itu target komunitas yang tepat buat game ekonomi.
- Bagian "What $SIN is not" (no yield, no income, no promised price) dan "Fair by design" (server decides, no pay-to-win) = disclaimer yang jelas, bukan boilerplate hukum.
- Klip gameplay asli = gak ada jurang antara marketing dan produk.
- Kontrol berdasarkan **posisi fisik tombol** (`KeyboardEvent.code`), jadi AZERTY otomatis jadi ZQSD. Semua tombol bisa di-remap, termasuk tombol mouse M3/M4/M5.
- Tanpa framework, HTML statis: cepat dan gak gampang rusak.

## Cara pakai di project gw
Tiap project (game, launchpad, mint): bikin halaman "rules/codex" yang angkanya diambil dari config yang sama dengan app (idealnya digenerate dari situ), plus bagian "apa yang BUKAN". Landing pakai rekaman produk asli.

## Caveat / jangan ditiru
- "Follows the code" cuma janji kalau halaman gak digenerate dari config. Sinkronisasi manual bisa ketinggalan.
- Video di landing nambah bobot halaman. Lazy-load + poster frame.

## Bukti
- `sindicat.game_codex.html.html` (snapshot recon): footer "the codex follows the code", tabel angka trade/bank/hideout/controls
- `sindicat.game.html` (snapshot recon): `/assets/tuto/*.mp4`, `/assets/tour/sin_earn.mp4`, teks "Five beats... all filmed in the game", "What $SIN is not", "Fair by design"
