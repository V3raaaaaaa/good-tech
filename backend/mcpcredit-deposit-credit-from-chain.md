---
name: Kredit deposit: webhook cuma petunjuk, server baca tx dari chain sendiri, unique per (tx, token account)
category: backend
project: mcp.credit (MCP Market)
chain: Solana mainnet
tags: [deposit, webhook, idempotency, solana, helius, reconciliation]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, source MIT di github.com/davidsyahshi/mcp-market
---

# Kredit deposit: webhook cuma petunjuk, server baca tx dari chain sendiri

## Ringkas
Payload webhook (Helius) gak pernah dipercaya, cuma dipakai buat tahu tx mana yang perlu dicek. Server ambil tx itu dari RPC, cek: mint = USDC/USDT asli, tujuan = token account alamat pool user, tx sukses, jumlah dari chain. Tiap pasangan (tx, token account) cuma bisa dikredit sekali (unique key). Ada tiga jalur yang ketemu di fungsi yang sama: webhook, tombol "check my deposit" di chat, dan cron 5 menit.

## Kenapa bagus
- Webhook palsu atau dobel gak bisa nambah saldo.
- Gak ada deposit yang hilang kalau webhook gagal (Helius retry cuma 3x): scan cron + on-demand.
- Dust (< 0.01) dicatat tapi gak dikredit, jadi spam dust gak mengotori saldo.
- Cron scan orang yang minta alamat 2 jam terakhir + potongan bergilir dari sisanya, jadi biaya RPC tetap kecil.
- Webhook bikin dan sinkronin dirinya sendiri (daftar alamat).
- Ada form "lost deposit" tanpa login (rate limit, satu per tx) buat kasus aneh.

## Cara pakai di project gw
Pola standar buat nerima pembayaran on-chain apapun (EVM/Solana): event/webhook = hint, sumber kebenaran = chain, idempotency key (tx, log index/account), plus rescan berkala.

## Caveat / jangan ditiru
- Bergantung ke satu provider RPC/webhook. Siapin fallback.
- Scan bergilir artinya deposit ke alamat lama bisa telat dikredit sampai giliran lewat.

## Bukti
- [server/src/deposits.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/deposits.js), [netlify/functions/deposits.mjs](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/netlify/functions/deposits.mjs), [server/test/deposits.test.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/test/deposits.test.js)
