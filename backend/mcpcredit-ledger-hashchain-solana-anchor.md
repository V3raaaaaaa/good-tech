---
name: Ledger append-only (trigger DB) + hash-chain + anchor memo di Solana, bisa diverifikasi di browser
category: backend
project: mcp.credit (MCP Market)
chain: Solana mainnet
tags: [ledger, audit-trail, hash-chain, anchoring, transparency, custodial]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, source MIT di github.com/davidsyahshi/mcp-market
---

# Ledger append-only + hash-chain + anchor memo di Solana

## Ringkas
Tiap perubahan saldo nulis baris ledger di transaksi DB yang sama. Database nolak UPDATE/DELETE di tabel ledger (trigger). Tiap baris punya `seq` dan `hash = sha256(prev_hash, seq, id, address, amount, kind, ref, time)`. Kira-kira tiap jam, kalau ada yang baru, payout wallet nulis hash terakhir ke Solana sebagai memo `mcp:anchor:<network>:<seq>:<hash>`. Halaman explorer download seluruh chain, ngitung ulang semua hash di browser, terus nyocokin sama memo yang diambil langsung dari RPC Solana.

## Kenapa bagus
- Sistem custodial jadi bisa diaudit siapa aja: ngubah/hapus/nyelipin baris lama ngerusak semua hash setelahnya, dan anchor di chain bikin gak bisa diulang dari awal tanpa ketahuan.
- Murah: satu memo (~0.00001 SOL) per jam, cuma kalau ada baris baru.
- Verifikasi jalan di browser user, bukan "percaya server".
- Semua deposit/withdraw nge-link ke tx Solana-nya.
- Jujur soal batas: "Neither can show that a row was honest when it was written."

## Cara kerja
```
ledger(seq, id, account, delta, kind, ref, at, hash)   trigger ledger_guard: BEFORE UPDATE OR DELETE -> raise
hash_n = sha256(entryText(hash_{n-1}, row_n))           genesis = 0x00…00
cron (hourly): if head > last_anchor -> sendMemo("mcp:anchor:mainnet:<seq>:<hash>") from payout wallet
GET /api/explorer/chain   -> semua baris; browser recompute + cek memo & signer via RPC
```

## Cara pakai di project gw
Buat app apapun yang nyimpen saldo/poin off-chain (game P2E, market, reward): ledger append-only + hash-chain + anchor periodik ke chain murah. Kasih halaman "Verify" di browser.

## Caveat / jangan ditiru
- Cuma ngebuktiin history gak ditulis ulang, bukan bahwa tiap baris jujur waktu ditulis.
- Kalau anchor berhenti, jaminannya cuma sampai anchor terakhir.
- Download seluruh chain di browser makin berat seiring waktu. Perlu checkpoint/snapshot.

## Bukti
- [server/src/explorer.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/explorer.js) (`entryHash`, anchors), [server/src/schema.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/schema.js) (`ledger_guard`)
- Anchor live: seq 26387 → tx `38LMsaUK…EmQQ3` (finalized 2026-11-08)
