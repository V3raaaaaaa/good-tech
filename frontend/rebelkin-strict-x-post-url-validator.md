---
name: Validator link X post yang ketat (pakai URL parser, bukan regex mentah)
category: frontend
project: RebelKin
chain: -
tags: [validation, url-parsing, x-api, input-hardening]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://rebelkin.xyz/post-link.js
---
# Validator link X post yang ketat

## Ringkas
Modul 12 baris (`post-link.js`) yang ngubah link X jadi post ID atau `null`. Dipakai buat ngunci tombol submit sampai link valid.

## Kenapa bagus
- Pakai `new URL()` dulu, baru cek bagian-bagiannya. Ini nutup trik klasik `https://x.com@evil.tld/...`, `https://x.com.evil.tld`, port aneh, atau `http:`.
- Hostname di-whitelist pakai `Set` exact match (`x.com`, `www.x.com`, `twitter.com`, `www.twitter.com`), bukan `endsWith`/`includes`.
- Path di-anchor penuh `^...$`, ID dibatasi digit 1–25, panjang input maksimal 250. Hasilnya cuma ID numerik, jadi data yang disimpan/ditampilin admin bersih.
- Ditulis sebagai ES module, jadi file yang sama bisa diimport di server (polanya enak buat validasi dua sisi).

## Cara kerja
```js
const hosts=new Set(['x.com','www.x.com','twitter.com','www.twitter.com']);
export function xPostId(value){
  if(typeof value!=='string'||value.length>250)return null;
  try{
    const url=new URL(value.trim());
    if(url.protocol!=='https:'||!hosts.has(url.hostname)||url.username||url.password||url.port)return null;
    return url.pathname.match(/^\/(?:[A-Za-z0-9_]+|i\/web)\/status\/(\d{1,25})\/?$/)?.[1]||null;
  }catch{return null;}
}
```
Di form: `field.setCustomValidity(field.value && !validPost ? 'Enter a valid X post link.' : '')` biar browser nampilin error native.

## Cara pakai di project gw
- Copy polanya buat field link apa pun (X post, Discord invite, GitHub repo): parse -> cek protocol -> host exact -> tolak userinfo/port -> regex path anchored -> return ID kanonik.
- Simpan ID-nya, bukan URL mentah, lalu bangun ulang URL kanonik pas ditampilin.
- Import modul yang sama di backend; jangan percaya validasi client doang.

## Caveat / jangan ditiru
- Ini cuma validasi format. Nggak ngebuktiin post itu ada, punya user itu, atau beneran repost. Mereka sendiri ngandelin review manual (`verificationEnabled:false` di `/api/config`).
- Nggak nerima `mobile.twitter.com`/`x.com/.../status/<id>/photo/1`; sesuaiin kalau mau lebih longgar.
- Whether backend-nya beneran pakai modul ini: unproven (server nggak publik).

## Bukti
- https://rebelkin.xyz/post-link.js
- https://rebelkin.xyz/app.js (`import {xPostId} from './post-link.js'`, fungsi `enabled()`).
