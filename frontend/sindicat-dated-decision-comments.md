---
name: Komentar kode yang nyatet tanggal + siapa yang mutusin + varian yang dipilih
category: frontend
project: SINDICAT
chain: -
tags: [dev-process, documentation, design-decisions, ai-assisted-dev]
score: 5
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) + play.sindicat.game.html
---

# Komentar kode yang nyatet tanggal + siapa yang mutusin + varian yang dipilih

## Ringkas
Tiap keputusan desain yang gak jelas ditulis langsung di kode, di tempat keputusannya berlaku, dengan format pendek: tanggal, siapa yang mutusin, dan varian mana yang dipilih dari beberapa prototipe. Contoh (nama orang gw ganti `<A>`/`<B>`): `(20/10, décision <A> sur le canevas « Barre du bas », option A)`, `(21/09, prise B du canvas « Loading screen » validée par <B>)`, `(27/09, demande <B>) LA PAGE D'ACCUEIL PASSE AVANT LA LANDING JOUABLE ...`.

## Kenapa bagus
- Developer berikutnya (atau AI agent) langsung tahu kenapa sesuatu begitu, jadi gak "dibenerin" balik ke versi yang udah ditolak.
- Alur "bikin beberapa varian (canvas A/B/C) → owner pilih → catat di kode" cocok banget buat kerja bareng AI: banyak opsi dibikin cepat, keputusannya tetap jelas siapa yang pegang.
- Gak perlu tool terpisah (Notion/Jira), dan ikut ke-version di git bareng kodenya.

## Cara pakai di project gw
Pas minta AI bikin UI/fitur: minta 2–3 varian, pilih, terus tulis komentar `(<tanggal>, keputusan <nama>: varian B — <alasan singkat>)` di kode. Buat keputusan lintas file, pakai satu `DECISIONS.md` (kayak forks.wiki) dan komentar pendek yang nunjuk ke sana.

## Caveat / jangan ditiru
- Komentar ini ikut ke bundle produksi (gak di-strip), jadi ngebocorin nama tim dan proses internal. Dari situ nama depan anggota tim bisa kebaca siapa aja. Strip komentar di build produksi (minifier `comments: false`), atau taruh di `DECISIONS.md` aja.
- Kalau gak dirawat, komentar lama jadi gak akurat.

## Bukti
- `game.js` (snapshot recon): ≥20 komentar bertanggal format "(20/09, décision <A>)" … "(23/09, décision <A> : « tout doit être uniformisé »)"
- `play.sindicat.game.html`: inline script "(27/09, demande <B>)"
