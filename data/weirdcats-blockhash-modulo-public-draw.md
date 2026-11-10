---
name: Undian off-chain yang bisa di-reproduce pakai blockhash Ethereum
category: data
project: Weird Cats
chain: Ethereum
tags: [randomness, raffle, provably-fair, blockhash, transparency]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://weirdcats.xyz/weirdlist/shelter/api.php?a=state + Ethereum mainnet blocks 26355823/26363306/26369509/26377137/26384502
---
# Undian off-chain yang bisa di-reproduce pakai blockhash Ethereum

## Ringkas
Event harian milih 1 dari 3 kandidat pakai `candidates[uint256(blockhash) % 3]` dari block Ethereum mainnet. API publik balikin `block` + `hash` + hasil, jadi siapa aja bisa cek ulang pakai RPC publik. Gak perlu kontrak, gak perlu VRF.

## Kenapa bagus
- Murah: nol gas, nol kontrak, nol oracle.
- Bisa diverifikasi: siapa pun cukup `cast block <n>` terus hitung modulo. Di project ini 5/5 hari cocok.
- Gampang dijelasin ke komunitas ("block publik yang milih").

## Cara kerja
1. Tiap hari punya `pets[3]`, `opens`, `closes`.
2. Setelah close, server ambil satu block Ethereum, simpan `block` + `hash` di state.
3. `winner = pets[int(hash, 16) % len(pets)]`.
4. Endpoint `GET /weirdlist/shelter/api.php?a=state` publikasi `days[].result = {pet, block, hash, free[], gtd[]}`.

Verifikasi:
```
cast block 26355823 -f hash --rpc-url <eth rpc>
# 0xed8d4124...403d  -> int % 3 = 0 -> pets[0] = lucky (cocok)
```

## Cara pakai di project gw
- **Wajib commit block number duluan**: umumin sebelum close, contoh "block pertama dengan timestamp >= closes + 10 menit" atau angka block spesifik. Taruh rumus itu di docs dan di API (`target_block`) sebelum event selesai.
- Pakai hash dari block yang cukup jauh di depan (beberapa menit) dan tunggu finality (~13 menit) biar gak kena reorg.
- Kalau pemilihannya lebih dari "pilih 1 dari N" (contoh pilih 5 pemenang dari daftar), publikasi daftar peserta (atau merkle root-nya) sebelum block keluar, lalu pakai `keccak(hash, i) % n` dengan algoritma yang ditulis di docs.
- Buat hadiah gede, mending on-chain VRF atau commit-reveal.

## Caveat / jangan ditiru
- Di project ini block number GAK di-commit: hari yang udah `closed` masih `block: null`, dan block yang dipakai jatuh 4,579-5,546 block (~15-18 jam) setelah close di jam yang acak-acakan. Operator bisa milih momen run draw dan nge-grind (block baru tiap 12 detik, peluang 1/3 hasilnya ganti).
- Cuma pemilihan pet yang reproducible; pemilihan pemenang spot dari adopter-nya gak didokumentasi dan daftar pesertanya gak dipublikasi.
- Proposer block bisa (secara teori) nahan block buat mempengaruhi hash; aman buat hadiah kecil, jangan buat hadiah bernilai tinggi.

## Bukti
- `https://weirdcats.xyz/weirdlist/shelter/api.php?a=state` (2026-11-10): hari 1-5 `{block, hash, pet}`; hari 6 `status: closed, block: null`.
- Hash dicek on-chain (Ethereum mainnet): 26355823 `0xed8d41...403d`, 26363306 `0x70e3a6...f3cb`, 26369509 `0x2e1fb3...466e`, 26377137 `0xfaa86a...003`, 26384502 `0x472f5b...81bb`; `int(hash) % 3` = index pet pemenang di kelima hari.
- `https://weirdcats.xyz/weirdlist/shelter/shelter.js` baris 211, 461 ("A public Ethereum block picks the pet").
