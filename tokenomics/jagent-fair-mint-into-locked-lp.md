---
name: Fair mint yang tiap pembayaran langsung jadi LP terkunci (80%) + harga bertingkat + floor line
category: tokenomics
project: $JAGENT (jager.live)
chain: BNB Smart Chain 56
tags: [fair-mint, liquidity, lp-burn, price-curve, floor, launchpad]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, source verified + eth_call
---

# Fair mint yang tiap pembayaran langsung jadi LP terkunci + harga bertingkat + floor line

## Ringkas
Gak ada presale/alokasi tim. Token cuma lahir waktu orang mint share (USDT/BNB). Sebelum pool buka (10.000 share pertama), token dikunci total (gak bisa transfer sama sekali), dan 80% pembayaran ditahan di kontrak. Di share ke-10.000, pool kebuka otomatis di tx yang sama (8.000 USDT + 400B token, LP ke dead address). Setelah itu tiap mint: 80% USDT + token di harga pool langsung ditambahin ke pair (LP ke dead), 20% ke treasury, dan minter dapet token baru senilai bayarannya di 99% harga pool. Harga share naik bertingkat 1 → 8.07 USDT. Kalau market value beredar jatuh di bawah `1.8 × total USDT dibayar`, mint ngebakar token dari pool buat naikin harga (maks +0.8%/tx, pool minimal 11.67B token).

## Kenapa bagus
- Likuiditas tumbuh bareng mint dan **gak bisa ditarik siapa pun** (99.9988% LP di dead address).
- Pembukaan pool deterministik (di share tertentu, di tx mint) = gak ada momen "dev nambah LP" yang bisa di-snipe.
- Lock transfer total sebelum pool buka = gak ada pool tiruan atau OTC pra-launch.
- Settle LP sekali per tx (dikumpulin dulu per share) = reserve sama persis kayak per-share, tapi gas lebih murah.
- Pajak dikumpulin di kontrak mint terus di-swap ke BNB pelan-pelan (maks 0.10% token pool per swap, sekali per blok, siapa aja bisa trigger).

## Cara pakai di project gw
Launch token tanpa presale: mint share bertarif yang langsung ngisi LP terkunci, pembukaan pool otomatis di threshold, transfer dikunci sampai pool buka, dan floor line yang dibiayai dari mint baru.

## Caveat / jangan ditiru
- Setelah pool buka, mint = beli token baru di 99% harga pool. **Gak ada edge buat minter**, dan kalau langsung dijual: 2% pajak jual + price impact. Di JAGENT, 24 jam terakhir: 2.339 buy vs 23.255 sell. Mayoritas aktivitas = mint lalu jual yang disubsidi reward invite.
- Arus beli-jual bersih di pool ≈ 0 (USDT pool ≈ total yang ditambahin dari mint). Harga ditopang mint baru, bukan pembeli organik.
- Floor line cuma jalan kalau ada yang mint. Kalau mint berhenti, gak ada yang jaga harga.
- Bergantung ke registrar Agent ID Binance + Chainlink + PancakeSwap.

## Bukti
- Mint [0x3643A907f875fA9B740e1C0747E91b5aA5222aB8](https://bscscan.com/address/0x3643A907f875fA9B740e1C0747E91b5aA5222aB8#code): `totalMinted`=186.463, `totalPaid`=582.207 USDT; pair reserve 473.970 USDT
- Konstanta: `OPEN_AT` 10.000, `TREASURY_BPS` 2000, `MINT_PRICE_BPS` 9900, `FLOOR_LINE`/`LINE_DENOM`, `RISE_NUM/DEN` 1008/1000, `POOL_TOKEN_FLOOR`, `TAX_SWAP_BPS` 10
