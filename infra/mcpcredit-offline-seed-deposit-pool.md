---
name: Pool alamat deposit dari seed offline, tiap alamat ditandatangani HMAC (server gak pegang key deposit)
category: infra
project: mcp.credit (MCP Market)
chain: Solana mainnet
tags: [custody, deposit, key-management, hmac, solana, hot-wallet]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, source MIT di github.com/davidsyahshi/mcp-market
---

# Pool alamat deposit dari seed offline, tiap alamat ditandatangani HMAC

## Ringkas
Owner bikin 10.000 alamat Solana di komputernya sendiri (bisa offline) dari seed 24 kata yang ditulis di kertas. Server cuma dapet **alamat publik** (CSV) + `DEPOSIT_POOL_KEY` yang diturunin dari seed, dan key itu cuma buat nandatangan daftar, gak bisa mindahin uang. Tiap user dikasih satu alamat. Sweep ke hot wallet dijalanin owner manual dari komputernya.

## Kenapa bagus
- **Server/DB jebol ≠ deposit hilang.** Gak ada private key deposit di server.
- **Alamat gak bisa ditukar:** server cuma nampilin dan ngekredit alamat yang HMAC-nya valid, jadi orang yang bisa nulis ke DB gak bisa nyelipin alamat sendiri.
- Gak perlu memo: satu alamat per user, jadi exchange pun bisa langsung kirim.
- Test server pakai devnet + seed beda. Campur uang test sama uang asli ditolak saat startup.
- Pool dipantau, ada warning kalau alamat kosong tinggal sedikit, dan bisa diperpanjang (`--start 10000`).

## Cara kerja
```
offline:  npm run deposit-pool -- --network mainnet     -> seed (kertas) + 10k alamat CSV + DEPOSIT_POOL_KEY
DB:       deposit_pool(address, index, mac = hmac(DEPOSIT_POOL_KEY, address|index|network))
server:   assign alamat ke user; tolak alamat yang mac-nya gak valid
owner:    npm run sweep (offline) -> hot wallet -> withdraw user
```

## Cara pakai di project gw
Buat app apapun yang nerima deposit (game, market, launchpad): turunin alamat dari seed/xpub offline, server cuma pegang alamat publik + MAC. Hot wallet terpisah, isinya dibatesin.

## Caveat / jangan ditiru
- **Hot wallet tetap jadi titik lemah.** Kode mereka sendiri bilang "keep little on it", tapi pas recon **98% reserve (.5k) ada di hot wallet**. Disiplin sweep/top-up harus otomatis (limit saldo), jangan manual.
- Sweep manual = withdraw bisa telat kalau owner gak online.
- Seed di kertas = satu titik kehilangan. Backup kebanyakan juga bahaya.

## Bukti
- [server/scripts/deposit-pool.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/scripts/deposit-pool.js), [server/scripts/sweep.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/scripts/sweep.js), [server/src/deposits.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/deposits.js)
- Reserve live `/api/explorer/summary`: payout $1522.74 vs deposit addresses $24.08 (2026-11-09)
