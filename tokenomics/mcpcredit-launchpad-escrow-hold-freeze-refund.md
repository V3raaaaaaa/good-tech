---
name: Launchpad NFT dengan escrow uang mint (hold min. 7 hari) + freeze yang refund penuh
category: tokenomics
project: mcp.credit (MCP Market)
chain: -
tags: [launchpad, escrow, anti-rug, refund, creator-payout]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, source MIT di github.com/davidsyahshi/mcp-market
---

# Launchpad NFT dengan escrow uang mint + freeze yang refund penuh

## Ringkas
Siapa aja bisa launch koleksi, tapi uang mint gak langsung ke creator: 10% ke market, sisanya masuk **escrow** (akun ledger sendiri) dan ditahan **minimal 7 hari per mint** (dikunci di kode: `HOLD_DAYS` gak bisa < 7). Owner yang release ke creator. Kalau koleksi ketahuan scam, owner **freeze**: mint + trading berhenti, dan semua mint yang masih di escrow **direfund penuh termasuk fee market**.

## Kenapa bagus
- Creator gak bisa langsung kabur bawa uang mint (rug paling umum di launchpad).
- Refund termasuk fee platform, jadi platform gak untung dari scam.
- Escrow dihitung di proof of reserves dan dicek konsisten sama hold yang jalan (`escrow_matches`).
- Batas bawah 7 hari ditegakkan di kode/setting, bukan janji.
- Review sebelum live: koleksi cuma keliatan creator + owner sampai disetujui.
- Gambar launchpad divalidasi pakai magic bytes (PNG/JPEG/GIF/WEBP, ≤1 MB, gak boleh SVG/HTML).

## Cara pakai di project gw
Launchpad apapun (NFT, token presale): escrow per mint dengan hold minimum, release bertahap atau setelah syarat, freeze = refund penuh termasuk fee. Kalau on-chain: kontrak escrow + timelock + refund path.

## Caveat / jangan ditiru
- Release dan freeze di tangan satu owner (custodial). Idealnya multisig atau aturan otomatis.
- Hold 7 hari gak ngelindungin dari rug yang pelan (creator nunggu release dulu).

## Bukti
- [server/src/launchpad.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/launchpad.js) (`LAUNCH_FEE_BPS` 1000, `HOLD_DAYS` ≥7), [server/test/launchpad.test.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/test/launchpad.test.js), trigger `mint_holds_guard` di [schema.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/schema.js)
