---
name: Trading lewat command X pakai wallet terpisah dengan policy signer terbatas (Privy)
category: security
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [agent, social-trading, privy, session-key, policy, x-commands]
score: 6
status: claimed
added: 2026-11-11
source: recon 2026-11-11, teks UI app
---

# Trading lewat command X pakai wallet terpisah dengan policy signer terbatas

## Ringkas
User bisa ngetik command di X buat beli/jual/hardwire/klaim. Setupnya: (1) link akun X, (2) buktiin kepemilikan wallet utama lewat sign pesan gratis (wallet ini cuma buat identitas, gak pernah sign trade), (3) isi **wallet trading terpisah** (Privy) dan atur batasnya. Policy signer per wallet cuma ngizinin: router kanonik QUOTRON dengan hasil balik ke wallet itu, hardwire V2, klaim reflections, dan (opsional) transfer saham ter-tokenisasi dengan cap ke penerima yang disebut.

## Kenapa bagus
- Wallet identitas ≠ wallet eksekusi, jadi kebocoran sesi bot gak nyentuh aset utama.
- Allowlist kontrak + tujuan output dikunci ke wallet itu = signer gak bisa dipakai buat kirim aset keluar sembarangan.
- Transfer saham dibatesin cap dan penerima eksplisit, dan default-nya mati.
- Pola "session key dengan policy" yang bisa dipakai di bot Telegram/X apa pun.

## Cara pakai di project gw
Bot trading/mint via sosial: pisahin wallet identitas dan eksekusi, policy signer = allowlist kontrak + selector + tujuan + cap, dan user yang ngisi dana di wallet eksekusi.

## Caveat / jangan ditiru
- **Status `claimed`:** cuma dari teks UI. Policy Privy di server gak bisa gw verifikasi dari luar.
- Wallet eksekusi custodial-ish (dipegang Privy/app). Isi secukupnya.

## Bukti
- Teks UI di app quotrons.cash: "The per-wallet Privy policy permits only the canonical QUOTRON router with proceeds returned to this wallet, V2 hardwire, V2 reflections claims, and — when enabled below — capped transfers of the ten supported tokenized stocks…"
