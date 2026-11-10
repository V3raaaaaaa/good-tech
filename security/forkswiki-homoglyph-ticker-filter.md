---
name: Filter ticker/nama anti-impersonation (homoglyph + leet + fonetik)
category: security
project: forks.wiki
chain: -
tags: [impersonation, homoglyph, filter, launchpad, anti-scam]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `config.js` (snapshot recon) (CONFIG.forkish)
---

# Filter ticker/nama anti-impersonation (homoglyph + leet + fonetik)

## Ringkas
Fungsi kecil yang nolak ticker/nama coin yang "kebaca atau kedengeran" kayak token resmi: FORK, F0RK, PHORK, FORQ, ФОРК (Kiril), ΦΟΡΚ (Yunani), "F O R K". Jalan di client dan server pakai config yang sama.

## Kenapa bagus
- Nutup trik impersonation yang umum: huruf Kiril/Yunani yang mirip, leetspeak, ejaan fonetik, dan spasi di antara huruf.
- Dicek per kata, jadi "Wolf Ork" gak ikut kena (sedikit false positive).
- Satu file config dipakai page dan Netlify Functions, jadi aturannya gak bisa beda antara UI dan server.

## Cara kerja
```
normalize NFKD, buang diakritik, lowercase
map Kiril/Yunani dua cara: SOUND (ф→f, р→r) dan LOOK (р→p, с→c)
leet: 0→o 1/!/|→i 3→e 4/@→a 5/$→s 7→t 8→b, buang non-huruf
fonetik: ph→f, ck→k, c/q→k, ou/oo/au/aw/uo→o, huruf dobel→satu
hit kalau /fork/ ada di salah satu versi; kalau ada kata ≤2 huruf, cek juga semua kata digabung
```

## Cara pakai di project gw
Bikin versi generik: daftar nama yang dilindungi (ticker sendiri + blue chip kayak USDC, USDT, SOL, ETH), jalankan normalisasi yang sama ke ticker dan nama, terus tolak kalau ada yang cocok. Taruh di server, jangan cuma di UI.

## Caveat / jangan ditiru
- Cuma ngelindungin nama mereka sendiri. Ticker "USDC" lolos 2x di platform yang sama, jadi blue chip juga harus masuk daftar.
- Coin palsu "FORK" sempet lolos sebelum filter ini ada, terus ditandain FAKE manual. Filter harus ada dari hari pertama.
- Regex `/fork/` setelah normalisasi bisa kena kata sah yang ngandung "fork" (misal "pitchfork"). Butuh allowlist.

## Bukti
- `config.js` (snapshot recon) (`CONFIG.forkish`, map `CYR` dan `LOOK`)
- Coin FAKE: `7BY8DJXdzmywdVhQVPsqZHpmwXJNyUpGcNbHjwXXfork` (`market.fake`)
