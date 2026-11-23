---
name: Trailing floor yang cuma pindah sekali sehari, high-water mark dicatat real-time
category: data
project: Breakout (breakoutprop.com)
chain: offchain
tags: [risk-engine, drawdown, high-water-mark, rollover, payout, ledger]
score: 7
status: verified
added: 2026-11-24
source: recon 2026-11-24, https://intercom.help/breakoutprop/en/articles/18514859-how-does-the-trailing-max-drawdown-work-on-spark002 , https://intercom.help/breakoutprop/en/articles/18514869-do-payouts-lower-my-high-water-mark-and-floor-on-spark002
---
# Trailing floor harian + high-water mark real-time

## Ringkas
Risk engine nyimpen dua angka per akun: `hwm` (equity tertinggi, di-update tiap tick) dan `floor` (batas breach). `floor` cuma di-set ulang di satu jam tetap (00:30 UTC) jadi `hwm - gap`. Di antara rollover, floor diam. Breach dicek ke equity (termasuk posisi terbuka) kapan pun, termasuk tepat setelah rollover.

## Kenapa bagus
- Satu titik waktu buat semua perubahan limit → gampang diaudit, gampang direplay, gak ada debat "floor gw pindah jam berapa".
- UI bisa nunjukin "limit lu besok" sebelum kejadian (field "Drawdown limit at 00:30 UTC").
- Payout diperlakukan konsisten: `hwm -= payout_gross` saat itu juga, jadi jarak ke floor gak berubah gara-gara narik profit.
- Dua varian cuma beda satu flag: hwm dari closed balance (v1) atau dari equity (v2).

## Cara kerja
```
on tick:      hwm = max(hwm, source)        # source = closed_balance (v1) | equity (v2)
              if equity < floor: breach()
on rollover:  floor = hwm - gap
              if equity < floor: breach()
on payout(x): hwm -= x ; next_floor -= x ; if floor > hwm - gap: floor = hwm - gap
              if equity_after < floor: minta konfirmasi dulu (payout bakal breach)
```
Biaya dan swap dipotong dari balance yang sama, swap dipecah 6× per hari (tiap 4 jam).

## Cara pakai di project gw
- Game/vault/leaderboard yang punya limit dinamis: pisahin "nilai yang dicatat terus" dari "limit yang berlaku", dan terapin limit di jadwal tetap.
- Selalu expose nilai limit berikutnya di API/UI.
- Aksi user yang bakal bikin breach (payout di sini) wajib lewat layar konfirmasi.

## Caveat / jangan ditiru
- Varian equity bikin user breach di rollover walau lagi profit: trade sempat +$2.000 lalu ditutup +$400 → floor naik ke atas equity → akun mati. Help center sampai butuh artikel khusus. Kalau lu niru, floor jangan pernah boleh loncat di atas equity sekarang (clamp ke `min(hwm - gap, equity)`), kecuali memang itu yang lu mau.
- Angka fee di docs tidak konsisten ("0.04 bps" vs "0.02%"). Tulis satuan sekali, di satu tempat.

## Bukti
- Contoh resmi: "Your floor moves to $50,500 … Your equity is below it, so your account is breached."
- Contoh payout: "you close at $53,000 and take a $3,000 payout. Your balance and high-water mark go back to $50,000, and your floor is $48,500."
