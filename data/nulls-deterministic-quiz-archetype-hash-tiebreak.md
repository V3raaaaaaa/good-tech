---
name: Assign archetype quiz yang deterministik dengan tie-break hash (bukan urutan array)
category: data
project: NULLS (nulls.world)
chain: -
tags: [quiz, determinism, fnv1a, personalization]
score: 5
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://nulls.world/ (inline app script, publik)
---
# Assign archetype quiz yang deterministik dengan tie-break hash (bukan urutan array)

## Ringkas
Lima pertanyaan, masing-masing empat pilihan. Tiap archetype (10) punya daftar "signals". Skor = jumlah jawaban yang cocok dengan signals. Kalau skornya seri, pemenangnya dipilih pakai `FNV-1a('quiz-v1:' + answers.join('')) % tied.length`, dan warna card dari hash yang sama plus suffix `:color`. Server menyimpan string jawaban (`"01320"`), jadi client bisa nge-rebuild player yang sama persis.

## Kenapa bagus
- Deterministik: jawaban sama selalu hasilnya sama, di device mana pun, tanpa perlu nyimpan hasil. Reload atau pindah browser gak ganti archetype.
- Adil buat yang seri: archetype yang kebetulan ada di awal array gak otomatis menang tiap kali seri, jadi distribusinya lebih rata.
- Prefix versi (`v1`) di key hash bikin aturan bisa diubah nanti tanpa diam-diam ngubah hasil lama.

## Cara kerja
```js
fnv1a = s => { let h = 2166136261; for (const c of s) h = Math.imul(h ^ c.charCodeAt(0), 16777619) >>> 0; return h; };
const key = 'quiz-v1:' + answers.join('');
const pick = tied[fnv1a(key) % tied.length];
const color = COLORS[fnv1a(key + ':color') % COLORS.length];
```

## Cara pakai di project gw
- Buat trait reveal, "which X are you", atau assign rarity kosmetik yang gak bernilai uang.
- Simpan input mentahnya (bukan cuma hasil), plus versi aturannya.

## Caveat / jangan ditiru
- Bukan randomness yang aman: hasilnya bisa diprediksi dan dipilih (cuma ada 4^5 = 1024 kombinasi). Jangan dipakai buat apa pun yang bernilai (rarity NFT, undian WL). Buat itu pakai VRF atau commit-reveal.
- Validasi input di server: array panjang 5, integer 0..3. Situsnya melakukan ini di client, tapi validasi di server belum terbukti dari luar.

## Bukti
- Script inline https://nulls.world/ : `memoryHash(text) { let hash = 2166136261; ... Math.imul(hash ^ char.charCodeAt(0), 16777619) >>> 0 }`, `const key = 'nulls-memory-v1:' + answers.join('')`, komentar "Stable ties use the entire answer sequence; array order never automatically wins a tie."
