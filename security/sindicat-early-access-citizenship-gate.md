---
name: Early access "citizenship": waitlist referral + wallet + kode, batas akun per device, guest session
category: security
project: SINDICAT
chain: -
tags: [early-access, waitlist, sybil, referral, privy, gating]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `admin-*.js` (snapshot recon) + game.js
---

# Early access "citizenship": waitlist referral + wallet + kode, batas akun per device

## Ringkas
Gate masuk game dalam beberapa lapis:
1. Pemain apply pakai X (Privy), klik "Follow @SindicatGame", isi wallet Robinhood Chain, terus share link referral.
2. Leaderboard referral publik ("most wanted"), diupdate tiap menit.
3. Admin promote "citizen" secara manual. Wallet-nya masuk list, tapi tetap butuh **kode** buat masuk game ("it never opens the game").
4. Server batesin akun per device (`deviceId` di localStorage, `429 too_many_accounts`) dan bisa ban/waitlist (`403`).

## Kenapa bagus
- Pisahin "dapat status/list wallet" dari "boleh main". Admin bisa ngatur gelombang masuk (wave) sesuai kapasitas server.
- Satu panel admin buat semua: gate on/off, bikin/matiin kode, waitlist sort referral + filter "via", lihat referral per orang, kasih kode massal, import list, export CSV citizen (handle + wallet).
- Jujur soal batas: UI admin bilang follow X **gak bisa dicek otomatis**, jadi harus dicek manual sebelum satu gelombang.
- Guest session (`guest:<uuid>`) bisa dipakai buat nyoba tanpa akun, dan bisa ditutup server (`guest_closed`).
- Privy kasih banyak cara login (X, email, wallet, passkey) dan `bind` ke akun yang ada (`409 taken` kalau identitas udah dipakai akun lain).

## Cara pakai di project gw
Launch game/app/NFT dengan antrian: referral leaderboard buat hype, wallet dikumpulin, tapi akses dibuka per gelombang pakai kode. Batesin akun per device + per identitas, dan sediain export CSV buat whitelist.

## Caveat / jangan ditiru
- Follow X yang cuma "diklik" = gampang dipalsuin. Butuh cek API X (berbayar) atau sampling manual.
- Referral leaderboard = insentif bikin akun X palsu.
- `deviceId` di localStorage gampang di-reset (incognito/hapus storage). Itu cuma rem ringan.
- Chunk admin ikut di-ship ke publik. UI-nya gak bahaya karena server cek role, tapi ngebocorin fitur dan alur internal.

## Bukti
- `admin-BLoBDi9b.js` (snapshot recon): string "Make them a citizen — their wallet goes on the list; it never opens the game", "Clicked « Follow @SindicatGame »... check by hand before a wave", "Citizens exported (CSV)"
- `game.js`: `adminCall('/early/gate'|'/early/codes'|'/early/waitlist'|'/early/citizens'|'/early/give-codes'|'/early/import')`, `openGuest`, `deviceId`, `too_many_accounts`
