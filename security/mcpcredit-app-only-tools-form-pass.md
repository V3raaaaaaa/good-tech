---
name: Tool sensitif cuma bisa dipencet user: MCP Apps visibility "app" + form pass HMAC
category: security
project: mcp.credit (MCP Market)
chain: Solana mainnet
tags: [mcp, ai-agent, prompt-injection, withdraw, mcp-apps, custodial]
score: 9
status: verified
added: 2026-11-11
source: recon 2026-11-11, source MIT di github.com/davidsyahshi/mcp-market
---

# Tool sensitif cuma bisa dipencet user: MCP Apps visibility "app" + form pass HMAC

## Ringkas
Di aplikasi yang dipakai lewat AI (connector MCP), aksi yang mindahin uang (withdraw, bind alamat, kirim NFT, burn) **gak dikasih ke AI**. AI cuma boleh buka *form* (MCP App) di chat. Tombol di form itu manggil tool yang ditandai `visibility: ["app"]`, jadi gak muncul di daftar tool AI. Dan biar aman di aplikasi yang ngabaikan flag itu, tiap tombol butuh **form pass**: token HMAC berumur pendek yang dikirim di `_meta` tool result (buat form, bukan buat konteks AI).

## Kenapa bagus
- **Kebal prompt injection.** Halaman web, file, atau nama NFT yang nyuruh "withdraw semua ke alamat X" gak bisa dieksekusi, karena AI emang gak punya tool-nya.
- **Pertahanan berlapis:** flag `visibility` (standar MCP Apps), pass HMAC (kalau host ngabaikan flag), dan AI gak bisa pre-fill alamat.
- **Alamat withdraw di-bind sekali**, ditandatangani HMAC di DB, dan baru bisa nerima **24 jam** setelah bind. Gantinya harus lewat support.
- Host yang gak bisa nampilin form = gak bisa withdraw sama sekali (fail closed).
- Pola yang sama dipakai buat transfer NFT dan burn: form dengan checkbox → Send → Confirm.

## Cara kerja
```
AI tool:    withdraw_form            -> result: UI resource + _meta.pass = "<exp>.<hmac(mcp-form:<net>:<user>:<exp>)>"
App tools:  withdraw_form_state / withdraw_form_bind / withdraw_form_submit   (visibility: ["app"], butuh pass)
bindMac  = hmac("mcp-bind:<user>:<address>:<setAt>")          // DB gak bisa disusupin alamat
rowMac   = hmac("mcp-w:<net>:<id>:<user>:<amount>:<fee>:<address>")
```

## Cara pakai di project gw
Buat connector MCP / agent apapun yang nyentuh uang atau aset (MCP mint, wallet bot, launchpad): pisahin tool **baca** (buat AI) dari tool **tulis bernilai** (cuma dari UI yang dipencet manusia). Kasih pass HMAC per user per sesi, dan delay buat alamat tujuan baru.

## Caveat / jangan ditiru
- `send_nft` (via chat) tetap bergantung AI nanya dulu. Gak ada tombol yang cuma bisa dipencet manusia di jalur itu.
- Masih custodial: owner bisa freeze/void. Ini ngelindungin user dari AI-nya sendiri, bukan dari operator.
- Butuh host yang support MCP Apps (Claude, ChatGPT). Klien lain gak bisa withdraw.

## Bukti
- [server/src/withdrawals.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/withdrawals.js) (form pass, bind/row HMAC), [server/src/mcp.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/mcp.js) (`visibility`, `tUiMeta`), [SECURITY.md](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/SECURITY.md)
