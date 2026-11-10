---
name: Proof of reserves live: held vs owed (balance + withdrawal + escrow) tiap 10 menit
category: data
project: mcp.credit (MCP Market)
chain: Solana mainnet
tags: [proof-of-reserves, transparency, custodial, accounting]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, /api/explorer/summary
---

# Proof of reserves live: held vs owed tiap 10 menit

## Ringkas
Endpoint publik yang tiap 10 menit ngitung: **owed** (total saldo user di ledger + withdrawal belum dibayar + escrow launchpad) vs **held** (USDC/USDT on-chain di semua alamat deposit, payout wallet, dan reserve wallet owner). Hasilnya coverage, `ledger_matches`, `escrow_matches`, dan daftar tiap akun on-chain (link Solscan).

## Kenapa bagus
- User bisa liat sendiri uangnya ada (coverage 1.027 pas recon) tanpa percaya laporan.
- Dua cek konsistensi internal: ledger vs saldo user, escrow vs hold yang masih jalan.
- Treasury owner dipisah dari utang ke user, jadi revenue owner gak "nutupin" utang.
- Rinci per wallet + per token, bukan cuma angka total.
- Jujur: reserve wallet owner ditulis sebagai "klaim owner" (Solscan nunjukin saldo, bukan siapa yang pegang key).

## Cara kerja
```json
"reserves": {"held_total":"1546825102","owed_balances":"1404133077","owed_withdrawals":"0","owed_escrow":"101700000",
             "owed_total":"1505833077","coverage":1.0272,"ledger_matches":true,"escrow_matches":true,
             "accounts":[{"kind":"payout","wallet":"3fmj…","token":"USDC","amount":"1522740000"}, {"kind":"deposit",...}]}
```

## Cara pakai di project gw
Buat app custodial apapun: endpoint reserves publik dengan rincian akun on-chain + cek konsistensi ledger. Tampilin di footer/explorer.

## Caveat / jangan ditiru
- Komposisi penting: 98% held di hot wallet = coverage 1.0 tapi risiko tinggi. Tampilin juga proporsi hot vs cold.
- Gak ngebuktiin liabilitas lengkap kalau ada utang di luar ledger (misal janji airdrop token).

## Bukti
- `GET https://mcp.credit/api/explorer/summary` → `reserves`
- [server/src/explorer.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/explorer.js)
