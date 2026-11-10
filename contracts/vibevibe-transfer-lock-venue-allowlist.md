---
name: Transfer token dikunci sampai graduate + allowlist venue
category: contracts
project: vibe/vibe (Seedify)
chain: Robinhood Chain Testnet 46630
tags: [launchpad, bonding-curve, anti-sniper, anti-rug, erc20, uniswap-v4]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, laporan recon internal
---

# Transfer token dikunci sampai graduate + allowlist venue

## Ringkas
Token hasil launch gak bisa di-transfer antar wallet selama masih di bonding curve. Cuma bisa beli/jual ke curve lewat router resmi. Setelah graduate baru kebuka, dan itu pun cuma boleh trading di venue (pool) yang di-allow.

## Kenapa bagus
- **Nutup pool palsu sebelum graduate.** Sniper/dev gak bisa bikin pool Uniswap sendiri di harga beda terus narik likuiditas.
- **Nutup distribusi diam-diam ke banyak wallet** (bundle/sybil) buat ngakalin wallet cap, karena token gak bisa dipindahin.
- `venueEnforcement` + `venueAllowed(address,bytes32,bool)` bikin token cuma "hidup" di pool resmi (poolId tertentu), jadi gak ada fragmentasi likuiditas dan gak ada honeypot pool tiruan.
- Unlock dipicu otomatis oleh graduation, bukan admin. `unlockTransfers()` revert buat semua orang sebelum waktunya.

## Cara kerja
- Token: `transfersUnlocked()` false → `transfer` revert (kecuali dari/ke curve, zap, locker).
- Graduation (tx user lewat zap) → locker `migrate` → token `unlockTransfers` → `transfersUnlocked() = true`.
- `externalVenues()` / `venueAllowed` dicek di hook transfer buat pool/router di luar allowlist.

## Cara pakai di project gw
Buat launchpad/token sendiri: override `_update` (OZ v5) supaya revert kalau `!unlocked && from != curve && to != curve && from != router`. Unlock cuma dari kontrak graduation. Tambahin allowlist pool kalau mau nge-lock likuiditas di satu venue.

## Caveat / jangan ditiru
- Wallet/aggregator yang gak ngerti lock bakal gagal transfer, dan user bingung. Perlu error yang jelas di UI (mereka punya `writeRefusalSentences`).
- Kalau graduation macet (target gak pernah kecapai), token selamanya gak bisa di-transfer. Siapin jalur exit (jual ke curve).
- Venue allowlist = sensor. Kalau allowlist bisa diubah admin, admin bisa matiin trading di DEX lain.
- Gak ngelindungin dari creator yang beli 49% di awal terus dump ke curve atau setelah graduate (lihat REPORT).
- Kontrak unverified: perilaku dibuktiin lewat simulasi `cast call`, bukan source.

## Bukti
- Token sample `0x0911b460f8ae4cdf9f76e42286bf44ae1862d8ae`: `transfer` revert `0xdb89e3f4`, `unlockTransfers` revert `0xd210afc7`, `venueEnforcement() = true`
- Token graduated `0x2cdf0c1c131bbc8624295ffcb4190a10c620bcfc`: `transfersUnlocked() = true`
