---
name: LLM ngusulin, API resmi yang verifikasi (1 call, cache per pertanyaan)
category: backend
project: forks.wiki
chain: -
tags: [llm, verification, github, graphql, cache, cost]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, [netlify/functions/trace.mjs](https://github.com/forkwiki/fork/blob/main/netlify/functions/trace.mjs)
---

# LLM ngusulin, API resmi yang verifikasi (1 call, cache per pertanyaan)

## Ringkas
LLM cuma dipakai buat ngusulin struktur (graf asal-usul repo). Semua node dicek ke GitHub dan yang gak ada dibuang, jadi halusinasi gak pernah sampai ke user. Murah: satu call model per pertanyaan baru.

## Kenapa bagus
- **Anti-halusinasi by design.** Model ngusulin, sumber kebenaran (GitHub GraphQL) yang mutusin. Link, star, tanggal diambil dari GitHub, bukan dari model.
- **Biaya rendah.** Ganti tool-loop 3+ call jadi 1 call JSON ~250 token (thinking off). Mereka ngukur hemat ~5x.
- **Gratis buat nambah isi.** Server nambahin fork terkenal (≥100 star dan ≥0.5% parent) langsung dari GitHub tanpa token model.
- **Server pegang prompt.** Endpoint cuma nerima pertanyaan, jadi API key gak bisa dipakai orang sebagai LLM gratis.
- Cache CDN 7 hari + memori, dan cuma pertanyaan baru yang kena rate limit per IP.

## Cara kerja
1. GitHub search buat kandidat (gratis, di-cache).
2. Satu call model, `response_format: json_object`, temperature 0.6, max 700 token, retry 1x kalau JSON jelek.
3. Satu call GraphQL ngecek semua repo (max 12 per request). Yang gak ada di-prune, nama dikanonikkan, duplikat digabung, record fork GitHub sendiri ditandain.
4. Tambah parent asli dan fork terkenal dari GitHub.
5. Cache: `netlify-cdn-cache-control: s-maxage=604800, stale-while-revalidate`, `netlify-vary: query=q`.

## Cara pakai di project gw
Pola umum buat fitur AI apapun yang outputnya harus faktual (token, contract, wallet, repo): model ngusulin kandidat dalam JSON, terus tiap item diverifikasi ke sumber resmi (RPC, explorer, API), dan yang gagal dibuang. Taruh prompt di server, cache per pertanyaan ternormalisasi.

## Caveat / jangan ditiru
- Relasi "inspired by / built on" dari model gak bisa diverifikasi GitHub, cuma keberadaan repo-nya. Graf bisa tetap salah secara makna.
- Hasil LLM ini ikut nentuin siapa dapet fee (ancestor), jadi salah tebak = duit ke orang salah. Di versi live mereka ganti ke owner + forker pilihan launcher.
- Rate limit pakai Map di memori function, jadi reset tiap cold start dan gak dibagi antar instance.

## Bukti
- [netlify/functions/trace.mjs](https://github.com/forkwiki/fork/blob/main/netlify/functions/trace.mjs), `netlify/lib/lineage.mjs`, `docs/DECISIONS.md`
- Live: `GET https://forks.wiki/api/trace?q=bitcoin`
