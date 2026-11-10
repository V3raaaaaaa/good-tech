---
name: Pack/loot provably fair pakai drand round masa depan + verifikasi BLS di browser
category: frontend
project: Yield Fields
chain: -
tags: [randomness, drand, bls12-381, provably-fair, rejection-sampling, noble-curves]
score: 9
status: verified
added: 2026-11-11
source: recon 2026-11-11, bundle publik https://yieldfields.fun/_next/static/immutable/chunks/1s_78nxc0fu1-.js dan 0nj6z90v558sh.js, https://yieldfields.fun/docs/reference/faq
---
# Pack/loot provably fair pakai drand round masa depan + verifikasi BLS di browser

## Ringkas
Setiap pembelian seed pack ("rip") diikat ke **drand quicknet round masa depan**. Setelah round keluar, browser user sendiri fetch beacon, **verifikasi tanda tangan BLS**-nya, terus ngitung ulang hasil pack dari randomness + `ripId`. Hasilnya dibandingin sama yang di-credit server (`match` / `mismatch`).

## Kenapa bagus
- Server nggak bisa milih hasil: randomness-nya belum ada waktu pembelian dicatat, dan datang dari jaringan drand (League of Entropy), bukan dari tim.
- Nggak butuh VRF on-chain (murah, nggak ada gas callback), tapi user tetap bisa verifikasi sendiri tanpa percaya API.
- Derivasi deterministik + domain-separated, jadi gampang diaudit dan dites.

## Cara kerja
- Config: `chainHash 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971` (quicknet), `genesisTime 0x64e62127`, `period 3`, `https://api.drand.sh/<chainHash>/public/<round>`.
- `DRAWS_PER_ROUND = 25`: rip berisi N pack butuh `ceil(N/25)` round berurutan.
- Per pack ke-i: seed = `keccak256("yf/seed/v1:${ripId}:${i}")`, digabung sama randomness round → angka 256-bit. **Rejection sampling**: tolak kalau `x >= 2^256 − (2^256 mod W)` (maks 256 percobaan), baru `x mod W`, lalu dipetakan ke tabel weight. Nggak ada modulo bias.
- BLS verify (G1 sig, DST `BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_`) pakai noble-curves, di-lazy-load di chunk terpisah biar bundle utama tetap kecil.
- UI nampilin status per round: `waiting` → `checking` → `valid`/`invalid`, plus link URL round biar user bisa cek manual.

## Cara pakai di project gw
- Waktu user beli: simpan `purchaseId`, hitung `targetRound = roundAt(now) + k` (k ≥ 2 biar pasti masa depan), commit ke DB/on-chain sebelum round keluar.
- Pakai `drand-client` atau noble-curves buat verify quicknet di client dan di server.
- Publish rumus derivasi + tabel weight biar orang bisa replikasi offline.

## Caveat / jangan ditiru
- Fairness tergantung server benar-benar commit round **sebelum** round itu publik. Kalau commit-nya cuma di DB, user harus percaya timestamp server. Lebih kuat kalau `purchaseId → round` di-emit on-chain atau di-log publik.
- Tabel weight bisa diubah server antar rip. Versikan (`v1` di domain tag) dan publish.
- Farming/pack di Yield Fields belum live di mainnet, jadi baru bisa diverifikasi kode client-nya.

## Bukti
- String `chainHash:"52db9ba7…"`, `DRAWS_PER_ROUND",0,25`, `yf/seed/v1:` dan logika "No draw fell below … in 256 attempts" di https://yieldfields.fun/_next/static/immutable/chunks/1s_78nxc0fu1-.js.
- noble-curves bls12-381 (`BLS_SIG_BLS12381G1_XMD`) di https://yieldfields.fun/_next/static/immutable/chunks/0nj6z90v558sh.js.
- Klaim docs: "Every pack is tied to a future draw from drand" (https://yieldfields.fun/docs/reference/faq).
