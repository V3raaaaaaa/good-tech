---
name: Pool vanity mint address (…fork) di-grind duluan
category: infra
project: forks.wiki
chain: Solana mainnet
tags: [vanity, branding, keypair, solana, launchpad]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, /api/health live
---

# Pool vanity mint address (…fork) di-grind duluan

## Ringkas
Semua coin yang di-launch lewat platform punya address yang berakhiran `fork`. Keypair-nya di-grind offline duluan, disimpan di DB terenkripsi, terus diambil satu per launch. Kalau pool habis, fallback ke address random.

## Kenapa bagus
- Branding gratis: siapa pun yang liat CA langsung tahu coin itu dari platform mana (kayak `…pump` di pump.fun, `…bonk` di letsbonk).
- Grinding mahal di-offload ke luar request, jadi launch tetap cepat.
- `/api/health` nunjukin stok pool (`free 2007, used 27, low false`), jadi gampang dipantau.

## Cara kerja
`scripts/mints.mjs` grind keypair dengan suffix tertentu, terus load ke tabel `mint_pool` (migrasi 0012) yang dienkripsi pakai `MINT_POOL_KEY`. Pas build, server ambil satu key, terus status-nya `used`, lalu `claimed` setelah coin live.

## Cara pakai di project gw
Kalau bikin launchpad atau factory NFT/token sendiri: grind suffix brand (Solana pakai `solana-keygen grind`; EVM pakai CREATE2 salt mining, kayak `0x…cafe`), simpan terenkripsi, dan ambil per deploy.

## Caveat / jangan ditiru
- Suffix gampang ditiru orang lain yang grind sendiri, jadi bukan bukti asal. Coin palsu "FORK" pakai suffix `…fork` karena memang di-launch lewat platform-nya, dan suffix gak nyaring itu.
- Server pegang private key mint sebelum dipakai. Di pump.fun key itu gak punya kuasa setelah create, tapi di chain/program lain belum tentu. Cek dulu authority-nya.
- Kode pool-nya (0012, `scripts/mints.mjs`) gak ada di repo publik, cuma kelihatan dari config + health.

## Bukti
- Live: `GET https://forks.wiki/api/health` → `launch.vanity`
- Config live: `config.js` (snapshot recon) (`vanity: 'fork'`)
- 27/27 coin berakhiran `fork` (`market.json` (snapshot recon))
