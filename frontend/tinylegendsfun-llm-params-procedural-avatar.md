---
name: LLM ngeluarin parameter terbatas, avatar dirender prosedural
category: frontend
project: Tiny Legends (tinylegends.fun)
chain: -
tags: [llm, structured-output, procedural-art, three-js, seeded-rng, cost]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://tiny-legends-production.up.railway.app/api/v1/legends + public JS bundle
---
# LLM ngeluarin parameter terbatas, avatar dirender prosedural

## Ringkas
"Bikin AI legend dari satu prompt" di sini gak pake image generation sama sekali. LLM cuma ngisi objek JSON terstruktur: nama, faction, 6 stat D&D-style, traits, lore 1 kalimat, sama `appearance` berisi enum + warna hex + multiplier (`headShape`, `armorStyle`, `helmetStyle`, `primaryWeapon`, `bodyColor`, `auraIntensity`, `widthMultiplier`, dst). Client lalu ngerender karakter 3D "bean" pake react-three-fiber dari parameter itu, plus RNG yang di-seed pake id legend buat detail yang gak diisi.

## Kenapa bagus
- Biaya per karakter = satu panggilan LLM teks kecil (prompt dibatasi 280 karakter), bukan image gen atau 3D gen.
- Art style 100% konsisten. Gak ada output aneh, NSFW, atau artefak gambar.
- Item kosmetik gampang ditempel karena slot-nya (hat, outfit, finish, trail, emote) cuma field di objek yang sama.
- Deterministik: `createRng("bean:"+legendId)` → legend yang sama selalu keliatan sama di semua device tanpa nyimpen aset.
- Ada migrasi schema: field gaya lama (`helmetStyle: visor/horned/crown/hood`, `armorStyle: plate/leather/robe/...`) dipetakan ke gaya baru (`cap/viking/crown/cat_ears`, pattern `split/belly/stars/...`), jadi legend lama ikut ke art direction baru tanpa regenerate.
- Error dari provider disaring: pesan yang cocok dengan `/GOOGLE_GENERATIVE|API_KEY|env var|schema|No object generated/i` diganti jadi "The forge is taking a breather... No creation slot was used." Detail config gak bocor, dan user tau kreditnya gak kepotong.

## Cara kerja
1. Brief dari client: `{inspiration, spark, emphasis?, prompt (≤280), name?}`.
2. Server manggil LLM dengan schema (pola error-nya cocok sama `generateObject` di Vercel AI SDK + provider Google; ini disimpulkan dari string error, belum terbukti).
3. Output disimpan sebagai row legend. Endpoint publik `/api/v1/legends` nunjukin bentuk JSON-nya.
4. Renderer: `beanLook(seed, appearance, flair)` → mesh primitif (sphere/cylinder/capsule) + material warna.

## Cara pakai di project gw
- Karakter/NFT/avatar "AI-generated": suruh LLM ngisi schema enum + range, jangan minta gambar. Validasi pake zod, clamp angka (mereka clamp multiplier ke 0.9–1.15).
- Seed RNG dari id buat semua detail sekunder.
- Simpan `artRevision`/versi schema biar bisa migrasi gaya nanti.
- Kalo generate gagal, jangan potong kuota (refund-before-charge, atau charge setelah sukses).

## Caveat / jangan ditiru
- Variasi visual terbatas sama jumlah enum. Kalo enum-nya dikit, karakter cepet keliatan mirip semua.
- Field `meshyStatus`/`customModelUrl` (kayaknya buat upgrade ke 3D gen Meshy) ada di API tapi nilainya null di semua 7.568 row. Fitur itu gak ada buktinya jalan.

## Bukti
- https://tiny-legends-production.up.railway.app/api/v1/legends?limit=1 (bentuk `stats`/`traits`/`appearance`/`flair`, `meshyStatus`)
- Bundle publik: export `forgeBrief` dan `forgeError` (regex di atas), `beanLook` dengan `createRng(\`bean:${id}\`)` dan mapping `{visor:"cap",horned:"viking",crown:"crown",hood:"cat_ears"}`
