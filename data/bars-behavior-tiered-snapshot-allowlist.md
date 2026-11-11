---
name: Allowlist bertingkat dari perilaku on-chain ("never sold"), root bisa direproduksi dari JSON publik
category: data
project: Bars (Jack Butcher / jack.art)
chain: Ethereum mainnet 1
tags: [allowlist, merkle, snapshot, anti-dump, phased-mint]
score: 8
status: verified
added: 2026-11-11
source: https://jack.art/exchange/bars-list.json (root 0x74f6b263…a561, block 26391637)
---

# Allowlist bertingkat dari perilaku on-chain ("never sold"), root bisa direproduksi dari JSON publik

## Ringkas
Snapshot 1 block: wallet dengan ≥1 token dan **gak pernah jual** masuk list. Tier: Day 1 = convert NFT / beli di auction / add liquidity; Day 2 = beli > 1 kali; Day 3 = sisanya; Day 4 = publik. JSON publik berisi block, blockHash, jumlah log, aturan dalam kalimat, daftar excluded & contract yang di-skip, dan 3 array address.

## Kenapa bagus
- Reward holder yang loyal, bukan yang paling kaya.
- Definisi jelas dan bisa dicek: "Sold = kirim token ke kontrak. Add liquidity bukan jual." Safe/smart wallet boleh, kontrak lain di-skip.
- Siapa pun bisa reproduksi root: leaf = `keccak256(keccak256(abi.encode(address, uint256 day)))`, pair = keccak dari 2 hash yang di-sort, node ganjil naik tanpa diduplikasi. Frontend juga bandingin root JSON vs `listRoot()` kontrak sebelum dipakai.
- Day N dibuka di `mintStart + N × 86400`. Tier atas boleh mint di hari berikutnya juga, cap `LIST_CAP` total.

## Cara kerja
```js
leaf = keccak256(keccak256(encodeAbiParameters([address,uint256],[wallet, day])))
pair = (a,b) => keccak256(a < b ? a ‖ b : b ‖ a)
levels: sort(leaves) → pair berpasangan → node ganjil di-carry
```
JSON di-cache-bust pakai `?v=<listRoot>`.

## Cara pakai di project gw
Phased mint/airdrop: publish JSON + aturan dalam kalimat + block hash, isi `listRoot` di kontrak, dan biarin UI/komunitas verifikasi sendiri.

## Caveat / jangan ditiru
- "Never sold" gampang di-game sybil: beli 1 token di banyak wallet sebelum snapshot. Di sini Day 3 berisi 17,072 wallet dengan median saldo cuma 2.8 token.
- Snapshot pagi hari H yang diumumin pas hari H juga = gak adil buat yang telat tahu, tapi sekaligus mencegah farming last-minute.

## Bukti
- Root direproduksi (snapshot recon): `0x74f6b263d3ddeb942f60b2a258d991ecaee2dbf9f2c17516a0cd27efebc1a561`, 18,304 address unik (223 / 1,009 / 17,072) → MATCH
- Kode builder `nx()`/`nw()` di `/exchange/bars/mint.js`
