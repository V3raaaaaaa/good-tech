---
name: Prepare → sign → submit dengan receipt UUID dari client
category: backend
project: Tiny Legends (tinylegends.fun)
chain: Solana (devnet)
tags: [idempotency, embedded-wallet, privy, solana, custodial-bridge]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, public JS bundle of https://tiny-legends-production.up.railway.app/wallet
---
# Prepare → sign → submit dengan receipt UUID dari client

## Ringkas
Buat mindahin saldo game (GRIT) atau NFT legend dari/ke wallet user, server yang bikin transaksi Solana-nya. Client cuma sign pake embedded wallet (Privy), terus balikin tx yang udah di-sign ke server. Tiap operasi bawa `receipt = crypto.randomUUID()` yang dibuat client, dan receipt yang sama dipake di fase `prepare` dan `submit`.

## Kenapa bagus
- Logika (amount, limit harian, fee payer, mint) semua di server. Client gak bisa nyusun instruksi aneh.
- Receipt dari client = idempotency key. Kalo jaringan putus antara sign dan submit, request bisa diulang tanpa dobel kredit/debit.
- UI punya state lengkap: `approval`, `sending`, `pending`, `sent`, `done`, `failed`, `expired`, `prepared`, `uncertain`, `cooldown`, `daily-limit`, `low-sol`. Ada juga pesan "An earlier request is still open. Check its receipt below before starting another." Jadi user gak nembak dua kali.
- Withdraw (game → wallet) gak butuh tanda tangan user (server yang kirim). Deposit/buy butuh sign. Arahnya dipisah dengan jelas.

## Cara kerja
1. Client: `receipt = crypto.randomUUID()`.
2. `POST /api/v1/agents/me/grit/{deposit|buy}` `{action:"prepare", receipt, amount|sol}` → server balikin `transaction` (base64, serialized). Kalo gak perlu sign, server langsung balikin hasil request.
3. Client decode base64 → `signTransaction({transaction, wallet, chain:"solana:devnet"})` lewat Privy.
4. `POST` lagi `{action:"submit", receipt, transaction:<signed base64>}`. Server verifikasi tx-nya sama dengan yang di-prepare, broadcast, terus nyatet status per receipt.
5. Pola yang sama dipake buat `POST /api/v1/agents/me/legends/{id}/nft/transfer {action:"prepare", receipt, to}`.
6. Server cek limit (`minGrit`, `dailyLimitGrit` per hari UTC) di prepare.

## Cara pakai di project gw
- Bridge custodial ↔ on-chain apa pun (poin game → token, saldo → NFT): server yang bikin tx, client cuma sign, idempotency key dari client.
- Simpan tabel `requests(receipt PK, kind, amount, tx_message_hash, status, sig)`. Di submit, cocokin hash message tx yang di-sign dengan yang di-prepare, tolak kalo beda.
- Treat `uncertain` sebagai state resmi (tx kekirim tapi konfirmasi belum ada), jangan langsung dianggap gagal.

## Caveat / jangan ditiru
- Yang keliatan cuma sisi client. Pengecekan "signed tx == prepared tx" di server gak bisa dibuktiin dari luar, jadi wajib lu implement sendiri.
- Masih devnet (`chain: null` di `/api/v1/grit/status`). Belum diuji di mainnet dengan uang beneran.
- Blockhash expiry: tx yang di-prepare kadaluarsa ~60–90 detik. Butuh state `expired` + re-prepare (mereka punya state-nya).

## Bukti
- Bundle publik halaman `/wallet` dan `/grit`: fungsi yang manggil `/api/v1/agents/me/legends/${id}/nft/transfer` dengan `{action:"prepare",receipt,to}` lalu `{action:"submit",receipt,transaction}`; `signTransaction(... chain:"solana:devnet")`.
- https://tiny-legends-production.up.railway.app/api/v1/grit/status (`chain: null`)
