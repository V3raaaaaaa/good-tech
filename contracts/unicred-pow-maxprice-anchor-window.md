---
name: PoW mint dengan domain-separated digest + maxPrice + 1 mint/block
category: contracts
project: UNICRED (unicred.fun)
chain: Unichain 130
tags: [pow, mint, nft, slippage, uniswap-v4]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-09-24
---

# PoW mint dengan domain-separated digest + maxPrice + 1 mint/block

## Ringkas
Varian PoW mint yang lebih rapi dari Hashcats: digest pakai domain + chainId + address NFT, ada `maxPrice` buat lindungin minter dari harga naik, dan cuma 1 mint per block.

## Kenapa bagus
- `DOMAIN, chainId, nft` di digest: solusi gak bisa di-replay ke chain atau contract lain (fork/clone).
- `mine(anchorBlock, nonce, maxPrice)`: tx revert kalau harga epoch udah naik pas tx landing. Ini slippage protection buat mint.
- Anchor window 250 block (~4 menit): solusi kadaluarsa tapi gak terlalu cepat.
- 1 mint per block bikin rate distribusi stabil.
- Mint #404 sekalian launch pool Uniswap v4 (pakai hook), jadi likuiditas otomatis.

## Cara kerja
```
challenge = keccak(abi.encode(blockhash(anchor), prevWork))
digest    = keccak(abi.encode(DOMAIN, 130, nft, challenge, miner, nonce))   // 192 byte
```
Difficulty = floor 24 bit + retarget (10 s, tiap 8 mint) + fieldStreak (+1/mint, −1 per 10 s idle, cap 16) + streak per miner.

## Cara pakai di project gw
Kalau bikin PoW mint: pakai format digest ini (domain separation) + param `maxPrice`. Dua hal itu murah dan nutup dua celah yang Hashcats biarin.

## Caveat / jangan ditiru
- 192 byte = 2 blok keccak. Kalau mau miner komunitas efisien, mending ≤ 136 byte. (Di sini block 1 bisa jadi midstate per job, jadi masih oke.)
- Gate "#404 reserved for team" cuma di UI (app.js), contract gak nge-gate. Kalau mau reserve, taruh di contract.
- `state()[8]` artinya "block ini udah ada mint", bukan "closed". Naming getter yang ambigu bikin bot (dan frontend) salah baca.
- Di Unichain tx diurutin by priority fee per flashblock 200 ms, jadi "1 mint/block" jadi tip war.

## Bukti
- NFT: `0xf60de24F228dc7Ca6fF025958d2eE3A956ED88E5` (Unichain 130)
- KAT 3/3 vs #201/#314/#315 dan view `digestOf`
- Kode: bot internal (gak di-share)
