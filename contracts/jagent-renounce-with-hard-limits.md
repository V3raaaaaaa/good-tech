---
name: Admin yang bisa di-renounce on-chain, dengan batas keras sebelumnya (gak bisa blok pair/EOA/7702, pause cuma sebelum launch)
category: contracts
project: $JAGENT (jager.live)
chain: BNB Smart Chain 56
tags: [admin-minimization, renounce, pause, pool-blocking, eip-7702, fair-mint]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, source verified (Sourcify exact_match)
---

# Admin yang bisa di-renounce on-chain, dengan batas keras sebelumnya

## Ringkas
Treasury (Safe) cuma punya tiga kuasa di kontrak mint: `seed` (sekali, isi USDT pembuka pool), `setPaused`, dan `setPoolBlocked`. Dari awal kuasa itu udah dibatasi: pool yang diblok **gak boleh** pair resmi, kontrak mint, treasury, token, dead address, address tanpa kode (EOA), atau wallet **EIP-7702** (dicek dari prefix `0xef0100`). `renounce()` matiin pause + blokir pool **selamanya** dan manggil `token.disableBlocks()`. Unpause/renounce juga baru bisa setelah `seeded && importLocked`.

## Kenapa bagus
- Kuasa darurat ada pas fase rawan (sebelum pool buka, migrasi), terus bisa dibuang permanen. Ini kebukti on-chain: `renounced()`=true, `blocksDisabled()`=true.
- Blokir pool gak bisa dipakai buat nge-freeze holder biasa. EOA dan wallet 7702 kebal by construction, jadi cuma kontrak pool liar yang bisa kena.
- Pajak (rate + penerima) di-hardcode di token, dan token gak punya `owner()`. Yang bisa mint cuma kontrak mint, dan gak bisa lewat cap.
- Pool V4 (PoolManager) dan Pancake Infinity Vault selalu ditolak, jadi gak ada pool tiruan di venue baru yang bisa ngakalin pajak.

## Cara kerja
```solidity
function _onlyTreasury() private view { require(msg.sender == treasury && !renounced); }
function setPoolBlocked(address pool, bool b) external { _onlyTreasury();
  if (pool==pair||pool==address(this)||pool==treasury||pool==address(token)||pool==DEAD
      ||unblockable[pool]||pool.code.length==0||_is7702(pool)) revert NotBlockable(); ... }
function renounce() external { _onlyTreasury(); require(seeded && importLocked);
  renounced = true; paused = false; token.disableBlocks(); }
```

## Cara pakai di project gw
Launchpad/token sendiri: kasih admin minimal dengan daftar "gak boleh disentuh" yang ditegakkan kode (termasuk EOA + 7702), syarat sebelum renounce, dan satu fungsi `renounce()` yang matiin semuanya sekaligus.

## Caveat / jangan ditiru
- Yang **gak** ikut di-renounce: `quotaSigner` (key server yang nandatangan quota sosial) dan semua reward off-chain (invite, ambassador, boss) yang dibayar dari treasury. Kontrak bersih, tapi ekonomi insentifnya tetap terpusat.
- Treasury tetap nerima 20% tiap mint + pajak tanpa batas pengeluaran.

## Bukti
- Mint [0x3643A907f875fA9B740e1C0747E91b5aA5222aB8](https://bscscan.com/address/0x3643A907f875fA9B740e1C0747E91b5aA5222aB8#code): `renounced()`=true, `seeded()`=true, `importLocked()`=true
- Token [0x8e6442663A4F8C50b6132c68d42A30E7DFE4Ae15](https://bscscan.com/address/0x8e6442663A4F8C50b6132c68d42A30E7DFE4Ae15#code): `blocksDisabled()`=true, `owner()` revert, `minter()` = kontrak mint
