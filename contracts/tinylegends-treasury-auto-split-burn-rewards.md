---
name: Treasury yang otomatis split tiap pembayaran ke burn + reward pool
category: contracts
project: Tiny Legends
chain: Robinhood Chain 4663
tags: [treasury, fee-split, burn, reward-pool, sink, game-economy]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, treasury 0x58e2430EdDCF639043a19a21a612520c268c82d4
---

# Treasury yang otomatis split tiap pembayaran ke burn + reward pool

## Ringkas
Semua pembayaran in-game (pack, rank, totem, item) masuk ke satu kontrak treasury. `settle()` ngebagi saldo token sesuai `burnBps` / `rewardsBps`: bagian burn dikirim ke dead/zero, bagian reward ke vault yang bayar pemain. ETH/USDC yang masuk bisa di-swap ke token dulu (`router`, `weth`) sebelum di-split.

## Kenapa bagus
- Sink dan sumber reward nyambung otomatis: tiap pemain bayar, pool reward pemain lain terisi dan supply berkurang.
- Split keliatan on-chain dan bisa dicek siapa aja (di sini 2500/7500, dan aliran 15.1M masuk → 11.1M ke vault + 3.7M burn cocok).
- `settle()` bisa dipanggil berkala (operator) jadi gak perlu logika split di tiap fungsi bayar.
- Satu tempat buat semua jalur bayar (LGND, ETH, USDC): "Every way of paying ends the same".

## Cara kerja
```solidity
burnBps = 2500; rewardsBps = 7500;          // setSplit(uint16,uint16)
settle(): bal = token.balanceOf(this); burn(bal * burnBps / 1e4); token.transfer(rewardsPool, bal * rewardsBps / 1e4)
setTargets(rewardsPool, team); setRouter(router); setWeth(weth)   // swap ETH -> token sebelum split
```

## Cara pakai di project gw
Launchpad/game/app yang punya fee: arahin semua fee ke satu splitter, split ke burn/reward/treasury. Buat split-nya **immutable** atau di belakang timelock, dan kasih event per settle.

## Caveat / jangan ditiru
- Di Tiny Legends `setSplit`, `setTargets`, dan **`withdrawEth(address,uint256)`** dikontrol satu EOA admin. Split bisa diubah dan ETH bisa ditarik kapan aja. "30/70" di UI vs 25/75 on-chain nunjukin angka udah pernah berubah.
- `router`/`weth` masih 0x0, jadi jalur swap ETH belum aktif. ETH yang masuk (0.64 ETH) nganggur dan bisa ditarik admin.
- Unverified: logika `settle` disimpulkan dari selector + aliran transfer, bukan source.

## Bukti
- Treasury `0x58e2430EdDCF639043a19a21a612520c268c82d4`: `burnBps()=2500`, `rewardsBps()=7500`, `rewardsPool()` = vault, `team()` = deployer, `router()=weth()=0x0`, saldo 0.64 ETH
- Aliran LGND: other→treasury 15.10M, treasury→vault 11.11M, treasury→zero 3.70M (`lgnd_transfers.json` (snapshot recon))
