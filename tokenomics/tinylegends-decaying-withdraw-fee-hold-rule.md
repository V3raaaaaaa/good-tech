---
name: Fee withdraw yang turun tiap hari nunggu + hold rule anti-dump
category: tokenomics
project: Tiny Legends
chain: Robinhood Chain 4663
tags: [p2e, withdraw-fee, anti-dump, anti-bot, vesting]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) (AB.EARN.wdFee)
---

# Fee withdraw yang turun tiap hari nunggu + hold rule anti-dump

## Ringkas
Fee withdraw tergantung berapa lama sejak withdraw terakhir: 10% kalau withdraw di hari yang sama, turun linear ke 0% setelah 7 hari. Ditambah "hold rule": baru boleh withdraw kalau wallet pegang ≥5000 token selama 24 jam, dan ada min withdraw + vesting singkat.

## Kenapa bagus
- Pemain sabar gak kena fee, farm bot yang withdraw tiap hari kena terus. Insentifnya langsung ke perilaku yang diinginkan, bukan sekadar larangan.
- Hold rule bikin bot harus beli dan pegang token dulu. Itu ada biaya modal per wallet dan sekaligus jadi buy pressure.
- Fee masuk ke treasury → burn + reward pool, jadi farmer nyubsidi pemain lain.
- NFT Founders bisa motong fee: perk yang ada nilainya buat holder.
- Vesting 30 menit (`notBefore` di voucher) = sempat ditinjau kalau ada yang aneh (server bisa balikin 403 "review").

## Cara kerja
```js
wdFee(last, now, nftFee) {
  d = last ? floor((now - last) / 1 day) : WD_FEE_DAYS          // 7
  f = WD_FEE_MAX * max(0, WD_FEE_DAYS - d) / WD_FEE_DAYS          // 10% -> 0%
  return f * (nftFee != null ? min(1, nftFee / WD_FEE) : 1)
}
withdraw: amount >= WD_MIN (500) && holdOk() (HOLD 5000, HOLD_H 24) && !WD_PAUSED && <= WD_CAP (70k)
```

## Cara pakai di project gw
Buat reward apapun yang bisa ditarik (game, quest, referral): fee yang turun linear terhadap waktu sejak withdraw terakhir + syarat hold. Tampilin di UI "tunggu N hari biar fee 0%".

## Caveat / jangan ditiru
- Semua aturan ini dicek di server/client, bukan di kontrak. Admin bisa ubah (`WD_PAUSED`, fee, cap) lewat panel.
- Hold rule dicek dari saldo wallet, jadi bisa diakalin dengan pinjam/flash token kalau cuma dicek sekali. Pakai `heldSince`/snapshot.
- Fee tinggi di token yang lagi jatuh = pemain kejebak dan marah.

## Bukti
- `AB.EARN` di `game.js` (snapshot recon): `WD_FEE_MAX:.1, WD_FEE_DAYS:7, HOLD:5e3, HOLD_H:24, WD_MIN:500, WD_CAP:7e4, WD_VEST_H:.5`
- String UI: "Daily caps, the hold rule, the 1-day unlock and the withdraw fee slow down farm bots and dumping."
