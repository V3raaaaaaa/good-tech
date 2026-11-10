---
name: ERC-404/hybrid: hapus approval per token di SETIAP perubahan owner (pelajaran exploit V1)
category: security
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [erc404, erc721, approval, invariant, exploit-lesson, dn404]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, post-mortem V1 + source V2 verified
---

# ERC-404/hybrid: hapus approval per token di SETIAP perubahan owner

## Ringkas
Di token hybrid ERC-20/ERC-721 (ERC-404, DN404), kepemilikan NFT bisa berubah lewat banyak jalur: transfer NFT, transfer ERC-20 (NFT larut/muncul), migrasi, recovery admin, ambil/balik dari pool. V1 QUOTRONS cuma hapus `getApproved(id)` di jalur transfer NFT. Jadi approval lama "selamat" waktu ID itu pindah lewat jalur ERC-20, terus bisa dipakai buat narik NFT dari pemilik baru. Itu kejadian **360 kali**. V2 nyatuin semua perubahan owner ke satu fungsi yang selalu hapus approval.

## Kenapa bagus
- Invariant yang jelas dan bisa dites: "setelah operasi apa pun yang ngubah `ownerOf(id)`, `getApproved(id) == 0` sampai pemilik baru approve lagi."
- Nutup satu kelas bug by construction, bukan by policy (ban kontrak exploit doang gak cukup, karena approval basi lain masih ada).
- Berlaku juga buat jalur admin (recovery) dan migrasi, yang sering kelupaan.

## Cara kerja
```solidity
function _setOwner(uint256 id, address to) internal {   // SATU-SATUNYA tempat ownerOf berubah
  delete _approved[id];                                  // selalu
  _ownerOf[id] = to; ...
}
// test: for each path in [mirrorTransfer, erc20Transfer(dissolve/materialize), migrate*, adminTransferTerminal, poolDraw/Return]
//   approve(X, id) -> path moves id -> assert getApproved(id) == 0 && X cannot transferFrom
```

## Cara pakai di project gw
Kontrak apa pun yang punya lebih dari satu jalur ngubah owner (NFT + token, staking yang wrap NFT, game item): pusatin mutasi owner di satu fungsi internal yang ngehapus approval, terus tulis test invariant buat tiap jalur.

## Caveat / jangan ditiru
- Approval operator seluruh wallet (`setApprovalForAll`) beda cerita. Itu tetap berlaku sampai dicabut user.
- ERC-404 tetap kompleks dan gampang bocor di jalur lain (rounding pecahan, reentrancy di sync). Butuh audit + fuzzing.

## Bukti
- [Post-mortem: exploit mechanics](https://github.com/mavrkofficial/quotrons-v1-post-mortem/blob/main/docs/01-incident/exploit-mechanics.md), [V2 security changes](https://github.com/mavrkofficial/quotrons-v1-post-mortem/blob/main/docs/04-v2/security-changes.md)
- Source V2: [0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F](https://robinhoodchain.blockscout.com/address/0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F?tab=contract)
