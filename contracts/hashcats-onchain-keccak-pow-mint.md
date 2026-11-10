---
name: On-chain keccak PoW mint (burst difficulty)
category: contracts
project: Hashcats (hashcats.fun)
chain: RobinHoodChain 4663
tags: [pow, mint, nft, difficulty, no-backend]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-09-12
---

# On-chain keccak PoW mint (burst difficulty)

## Ringkas
Mint NFT tanpa backend, captcha, atau whitelist: yang mau mint harus nemu nonce yang hash-nya di bawah target. Semua dicek di contract.

## Kenapa bagus
- Gak ada server yang bisa down, di-DDoS, atau dicurangi admin. Fair launch beneran.
- Target selalu `2^n − 1`, jadi cek di contract = "≥ N leading zero bits", murah gas.
- Preimage pas 116 byte = 1 permutasi keccak-f1600, jadi miner GPU efisien (enak buat komunitas).
- Difficulty adaptif: ngerem burst mint tanpa perlu admin.

## Cara kerja
```solidity
work = keccak256(abi.encodePacked(msg.sender, nonce, prevWork, anchor));
require(work < targetFor(msg.sender));
// mine(uint256 nonce, uint256 anchorBlock) payable
```
- `prevWork` = work cat terakhir: tiap mint ngerubah puzzle berikutnya, gak bisa pre-mine.
- `anchor` = (block, blockhash) terbaru: solusi kadaluarsa.
- `msg.sender` di preimage: solusi gak bisa dicuri dari mempool.
- `currentTarget = baseTarget >> currentBurst`. Burst global +1 per mint, −1 per 10 s, cap 16. Retarget tiap 8 mint ke interval 10 s.
- `personalBurst(miner)` numpuk per address (rem whale per wallet).

## Cara pakai di project gw
Template bagus buat fair launch NFT/token tanpa infra. Preimage tetap ≤ 136 byte (1 blok keccak) biar miner simple. Masukin `msg.sender` + `prevWork` + anchor blockhash, itu tiga hal yang bikin gak bisa di-front-run atau pre-mine.

## Caveat / jangan ditiru
- `personalBurst` per address gampang dilewati dengan rotate wallet. Kalau mau anti-sybil, PoW doang gak cukup.
- GPU farm menang telak (network ~2.5 TH/s pas diukur). "Fair" artinya fair buat yang punya hashrate, bukan buat retail.
- Harga dobel tiap epoch: kurva bikin hype awal, tapi epoch akhir gak masuk akal ekonominya.

## Bukti
- Contract: `0xca75df55cc9c476db27a7375d1fc8e794cf80721` (RHC 4663)
- Preimage dicocokin byte-per-byte sama tx winning cat #376
- Kode miner: internal (gak di-share)
