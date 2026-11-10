---
name: "Hardwire": burn unit likuid jadi NFT permanen yang dapet bagian fee (dibayar saham ter-tokenisasi) + gacha reroll
category: tokenomics
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [erc404, burn, reflections, gacha, tokenized-stocks, flywheel]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, subgraph + source verified
---

# "Hardwire": burn unit likuid jadi NFT permanen yang dapet bagian fee + gacha reroll

## Ringkas
Tiap unit selalu ada di salah satu dari dua keadaan: **likuid** (token yang bisa ditrade dan di-reroll, NFT "dark" gak dapet apa-apa) atau **hardwired** (token di-burn, NFT jadi permanen dan dapet reward). Fee 3% dari trading float likuid dibayarin ke set hardwired, dalam bentuk saham ter-tokenisasi (10 saham, satu saham per "track" isi 444 mesin). "Fee stream dihasilkan float likuid dan dikonsumsi set hardwired. Tiap hardwire mindahin satu unit dari sisi penghasil ke sisi konsumen. Ketegangan itu adalah desainnya."

## Kenapa bagus
- **Komitmen satu arah yang jelas:** burn = kehilangan likuiditas, dapet klaim permanen ke aktivitas trading. Bukan "staking" yang bisa di-unbond.
- **Gacha yang jujur:** terminal muncul acak dari pool. Odds = komposisi pool yang publik, dan randomness-nya diakui pseudorandom dari state block.
- **Insentif seimbang per track:** tiap track dapet budget WETH sama. Track yang sedikit hardwire = bagian per terminal lebih gede, jadi orang terdorong nyebar.
- Reward di NFT ikut pindah kalau NFT dijual (accumulator ala masterchef).
- Angka nyata: 3.440/4.444 di-hardwire, 304 ETH udah dikonversi ke saham.

## Cara pakai di project gw
Buat koleksi/token apa pun dengan fee: kasih mekanik "kunci permanen" (burn token → NFT yang dapet bagian fee) daripada staking. Tampilin odds gacha dari state on-chain.

## Caveat / jangan ditiru
- **Dilusi:** tiap hardwire baru nambah penerima dan ngurangin float yang ngehasilin fee. Yield awal gak representatif, dan kalau volume mati, hardwired dapet nol.
- Reward bergantung keeper + saham ter-tokenisasi pihak ketiga yang upgradeable dan dibatesin di US.
- Penjual bisa klaim pending reward tepat sebelum jual. Pembeli harus cek saat eksekusi.

## Bukti
- Token `hardwire()`, `totalHardwired()`=3440: [0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F](https://robinhoodchain.blockscout.com/address/0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F?tab=contract)
- Subgraph `quotrons-v2-extended`: totalWethToReflections 304.33 ETH, totalConvertedWeth 304.3 ETH, 2.631 epoch
