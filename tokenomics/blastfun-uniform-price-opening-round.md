---
name: Opening round harga seragam (batch buy) buat lawan sniper di bonding curve
category: tokenomics
project: Blast (blast.fun)
chain: sui
tags: [anti-sniper, bonding-curve, batch-auction, fair-launch, move]
score: 9
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://github.com/interest-protocol/blast-v2-contracts (docs/decisions/0093-optional-opening-round.md, sui/launch/launchpad/sources/launch/launch.move), https://docs.blast.fun/launchpad/trading/
---
# Opening round harga seragam (batch buy) buat lawan sniper di bonding curve

## Ringkas
Opsional per launch: selama 60–300 detik setelah launch publik, nggak ada buy/sell. Semua orang (termasuk creator) setor quote ke satu pot. Begitu window habis, siapa aja bisa `settle`: pot dibeli **sekali** dari curve. Setiap bidder dapet bagian token pro-rata dari bid-nya, jadi harga rata-ratanya sama buat semua.

## Kenapa bagus
- Argumen di ADR-nya tajam: cap per-wallet itu "ngejatah berdasarkan identitas", padahal address gratis bikinnya, jadi sniper tinggal split ke banyak wallet. Batch harga seragam ngejatah berdasarkan **modal**. Split ke banyak wallet nggak ngubah apa-apa, dan urutan datang dalam window juga nggak ngaruh. Perang gas/MEV di blok pertama jadi nggak ada gunanya.
- Creator nggak bisa beli duluan di harga termurah. Bid creator masuk pot yang sama.
- Bid nggak bisa ditarik, jadi nggak bisa pasang bid gede buat pura-pura ada demand terus kabur.
- Penjelasannya cukup satu kalimat buat trader.

## Cara kerja
- `set_opening_round(ms)` waktu create (0 = mati; 60k–300k ms). Lifecycle mulai dari `OpeningRound`.
- `join_opening_round(coin)`: `bid[sender] += amount` (dynamic field `OpeningRoundBidKey(sender)`), plus total `opening_round_bids`.
- `settle_opening_round` (siapa aja, setelah window): lifecycle → `Live`, `buy_from_curve(pot, min_out=0)` lewat jalur, fee dan graduation cap yang sama kayak `buy`; meme hasil beli + sisa quote (kalau lewat target) ditahan.
- `deliver_opening_round(bidder)` (siapa aja, kapan aja sesudahnya): `meme * bid / total_undelivered`, dibulatkan ke bawah. Delivery terakhir dapet sisanya. Bayarnya selalu ke bidder, nggak pernah ke pemanggil.
- Kalau pot langsung nembus graduation target, curve langsung `MigrationReady`.

## Cara pakai di project gw
- Launchpad EVM/Solana: ganti "anti-snipe tax" atau "max wallet" dengan fase deposit N detik plus satu swap batch. Di EVM: `deposit()` → `settle()` panggil router/curve sekali → `claim()` pro-rata (pola pull, biar nggak looping transfer).
- Bisa juga dipake buat NFT/mint: fase komit dengan harga seragam, lalu alokasi pro-rata dengan refund sisa.

## Caveat / jangan ditiru
- Pot nggak punya `min_out` per bidder. Kalau lu bikin curve dengan virtual reserve ekstrem, pastiin harga awal masuk akal.
- Yang manggil `settle` bisa langsung `buy` di PTB/blok yang sama sebagai trader pertama setelah pot. Itu wajar, tapi jangan diklaim "nol keunggulan".
- Kalau mau pakai pola push, delivery butuh 1 tx per bidder. Lebih aman pull/claim.
- Kode Blast-nya BUSL-1.1. Tiru mekanismenya, tulis kode sendiri.

## Bukti
- ADR: https://github.com/interest-protocol/blast-v2-contracts/blob/main/docs/decisions/0093-optional-opening-round.md
- Implementasi: `sui/launch/launchpad/sources/launch/launch.move` (`join_opening_round`, `settle_opening_round`, `deliver_opening_round`)
- Docs user: https://docs.blast.fun/launchpad/trading/
- Status: kode udah di-publish di package `0x9c2cef371c0e80648136f7ae65378ac9476e3fdb860538d00290e6e4f975b192` (Sui mainnet), tapi launchpad masih paused, jadi belum ada opening round live.
