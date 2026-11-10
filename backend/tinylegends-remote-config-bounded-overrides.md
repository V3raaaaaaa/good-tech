---
name: Remote config live dengan skema min/max/type + endpoint harga ber-flag stale
category: backend
project: Tiny Legends
chain: -
tags: [remote-config, live-ops, feature-flags, oracle, game-economy]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) (AB.SETTINGS apply/pull, AB.Price)
---

# Remote config live dengan skema min/max/type + endpoint harga ber-flag stale

## Ringkas
Semua angka balance game didaftarin di satu skema (`AB.SETTINGS`: key, group, label, type, min, max). Client narik `/config` tiap 10 menit dan cuma nerima override yang lolos validasi skema. Kalau override dihapus, nilainya balik ke default asli (di-snapshot pas pertama load). Harga token diambil dari `/price` yang bawa sumber + flag `stale`, dan fitur bayar dimatiin kalau harga basi.

## Kenapa bagus
- Live-ops tanpa deploy: tim bisa nyetel ekonomi dalam hitungan menit.
- **Validasi min/max/int di client** = typo admin (misal 1000x) gak bisa bikin game rusak. Nilai di luar batas diabaikan, bukan dipakai.
- Snapshot default + `resetMissing` = hapus override langsung balik normal, gak ada nilai nyangkut.
- `price.<sku>` override buat harga toko dalam USD (0–100k).
- `AB.Price.live()` = harga dianggap valid cuma kalau `lgndUsd > 0 && !stale && umur < 10 menit`. Tanpa itu, pembayaran yang butuh konversi gak jalan.
- Admin panel otomatis dari skema (`list()` balikin label, group, min, max, def, value).

## Cara kerja
```js
SETTINGS = [{key:"earn.dayUsd", path:"EARN.DAY_USD", type:"num", min:0, max:..., group, label}, ...]
apply(overrides): for s of SETTINGS: want = ok(s, overrides[s.key]) ? +overrides[s.key] : defaults[s.key]; set(s, want)
pull(): every 10 min GET /config -> {overrides:{"earn.dayUsd":100,"earn.maxDayLgnd":1000000}, at}
GET /price -> {lgndUsd, ethUsd, src:"dexscreener/dexscreener", stale:false, pay:["lgnd","eth"], at}
```

## Cara pakai di project gw
Game/app dengan ekonomi (mint radar alert threshold, mini game reward, launchpad fee): satu skema setting dengan batas, override dari server, dan default yang bisa dibalikin. Endpoint harga selalu bawa `src` + `stale` + `at`.

## Caveat / jangan ditiru
- **Remote config buat angka yang nentuin uang = kuasa admin tanpa batas.** Tiny Legends naikin `earn.dayUsd` dari 1.25 ke 100 secara live. Buat parameter ekonomi yang nyangkut token, taruh di kontrak dengan timelock, atau minimal publikasikan changelog.
- Validasi cuma di client. Server harus pakai skema yang sama, kalau nggak, client dan server bisa beda angka.
- Oracle dari DexScreener pool kecil = gampang dimanipulasi. Kasih TWAP atau batas perubahan.

## Bukti
- `game.js` (snapshot recon): `apply`, `snapshot`, `ok`, `list`, `pull` (6e5 ms), `AB.Price.live`
- `GET https://api.tinylegendsgame.io/config`, `GET /price`
