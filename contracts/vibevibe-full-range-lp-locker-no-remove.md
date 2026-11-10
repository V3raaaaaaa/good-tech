---
name: LP graduation full-range dikunci di locker tanpa fungsi remove
category: contracts
project: vibe/vibe (Seedify)
chain: Robinhood Chain Testnet 46630
tags: [uniswap-v4, lp-lock, graduation, anti-rug, immutable]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, graduation tx 0x279b47094902dbde7ea276d025784deb3739946a51a8b54b5d9bf81703197829
---

# LP graduation full-range dikunci di locker tanpa fungsi remove

## Ringkas
Pas graduate, ETH + token dari curve langsung dimasukin ke posisi full-range Uniswap v4 atas nama kontrak locker. Locker gak punya fungsi buat narik likuiditas, dan `migrate` cuma bisa dipanggil sekali oleh curve token itu.

## Kenapa bagus
- "Locked forever" by design, bukan janji: gak ada fungsi `withdraw/remove/decreaseLiquidity` di bytecode locker.
- Di v4 posisi dimiliki `sender` dari `modifyLiquidity`, yaitu locker, jadi gak ada NFT LP yang bisa dipindahin.
- Hook juga pasang `beforeRemoveLiquidity` sebagai lapis kedua.
- Full-range (−887220…887220) = gak ada range yang bisa "keluar" dan bikin harga kosong.
- Kontrak bukan proxy, jadi gak ada upgrade yang bisa nambahin fungsi remove nanti.

## Cara kerja
```
curve.complete -> zap -> locker.migrate(token)   // cek msg.sender == curveOf(token), seeded[poolId] == false
  poolManager.unlock -> modifyLiquidity(full range, +L)  // sender = locker
  seeded[poolId] = true; token.unlockTransfers()
```
Bukti: `migrate` dari random/Safe/factory/token → `Unauthorized()`; dari curve setelah graduate → error lain (sekali pakai).

## Cara pakai di project gw
Buat launchpad yang janjiin LP lock: jangan pakai locker berwaktu atau multisig. Bikin kontrak locker kecil yang cuma bisa `add` (dan opsional `collect fees` ke penerima tetap), tanpa remove, tanpa owner, tanpa proxy. Di v2/v3: kirim LP token/NFT ke kontrak tanpa fungsi transfer keluar, atau burn LP token-nya.

## Caveat / jangan ditiru
- Fee LP v4 tetap nempel di posisi. Kalau locker gak punya `collect`, fee itu hilang selamanya (atau di sini diambil lewat hook).
- Kalau ada bug di pool/hook, likuiditas gak bisa diselamatkan.
- Full-range di v4 kurang efisien modal dibanding range konsentrasi.
- Unverified: kesimpulan "gak ada remove" dari daftar selector, bukan source.

## Bukti
- Locker `0xcF7D6547bc11992a6c492e508E701c79B8393930` (12 selector: `migrate`, `lockedPositions`, `seeded`, `poolKeyOf`, `poolIdOf`, `unlockCallback`, …)
- `ModifyLiquidity` sender = locker, tick ±887220, liq 28284271247461900976033 (laporan recon internal)
