---
name: Mint recipe dari tx sukses + replay eth_call dengan state override
category: data
project: Mint Radar (punya sendiri)
chain: BSC 56
tags: [indexer, eth_call, state-override, recon, automation]
score: 8
status: verified
added: 2026-11-11
source: tool internal, fase 3 (2026-10-31)
---

# Mint recipe dari tx sukses + replay eth_call dengan state override

## Ringkas
Cara otomatis tahu "gimana cara mint contract ini" (selector, gate, harga, gas) tanpa baca source: ambil tx mint yang sukses, decode, lalu replay pakai `eth_call` dari wallet random dengan saldo palsu.

## Kenapa bagus
- Jalan buat contract unverified sekalipun.
- `eth_call` + state override (kasih saldo BNB ke wallet random) = tes gratis, gak ada tx beneran.
- Replay dari wallet random vs wallet yang punya gate (misal .ai holder) langsung kasih tahu jenis gate-nya.

## Cara kerja
1. Ambil tx sukses ke contract, decode calldata (selector + args + value).
2. Replay `eth_call` dengan `stateOverride: {<random>: {balance: ...}}` → lolos = open.
3. Replay dari holder gate → bedain `agent_only`, unique-arg, signature/voucher.
4. Simpan hasil: selector, gate, price, gas, per-wallet.
Dicek vs tx mint yang hasilnya udah diketahui: POA agent_only, Hashstone unique-arg 2/wallet, NONCE signature 2/wallet.

## Cara pakai di project gw
Buat tool apapun yang perlu "ngerti" contract orang (radar, copy-trade, auditor). Juga bagus buat testing contract sendiri: replay semua jalur mint dari berbagai jenis wallet sebelum launch.

## Caveat / jangan ditiru
- `gate: open` cuma artinya gak ada voucher di calldata, bukan pasti bebas.
- Gak semua RPC support state override (publicnode support).
- Contract bisa nyimpen harga dalam token lain (misal `PRICE()` dalam USDT), jangan langsung anggap BNB.
- Pelajaran RPC dari project yang sama: node bisa balikin list kosong **tanpa error** buat query log. Failover jangan percaya hasil kosong; recount vs DB.

## Bukti
- Kode: tool internal (gak di-share)
- Audit nama: script internal yang ngitung ulang hasil indexer vs DB
