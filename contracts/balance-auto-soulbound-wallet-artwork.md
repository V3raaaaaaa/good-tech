---
name: Wallet-bound ERC-721 yang auto-mint pas address pertama kali nerima token
category: contracts
project: BALANCE / Exchange (Jack Butcher)
chain: Ethereum mainnet 1
tags: [erc721, soulbound, onchain-svg, erc20-hook, holder-art]
score: 6
status: verified
added: 2026-11-11
source: verified source Etherscan 0x3620540c… (LineageArtwork.sol) + artwork 0x3F2BA6C00c386986686A429c52099AaCD51b7e38
---

# Wallet-bound ERC-721 yang auto-mint pas address pertama kali nerima token

## Ringkas
Hook `_update` di ERC-20 manggil `artwork.balanceChanged(from, to)`. Kalau `to` belum pernah nerima, kontrak artwork mint NFT "Balance #N" (urutan first-receipt) yang gak bisa ditransfer/approve. SVG + metadata full on-chain dan update ngikutin saldo, ink, dan history (peak, emptied, returnsFromZero).

## Kenapa bagus
- Tiap holder otomatis punya "kartu" tanpa claim/mint terpisah. Viral loop: beli 1 token = dapet NFT.
- Metadata ngitung statistik perilaku (transfer in/out, times emptied) langsung dari state token.
- NFT tetap ada walau saldo 0, nomor urut jadi semacam "holder #".

## Cara kerja
- `LineageWithdrawals._update` → setelah update ink + `StoredHistory`, panggil `artwork.balanceChanged`.
- Artwork mint id baru kalau address belum punya; reserve dikecualikan; transfer/approve revert.
- `tokenURI` render SVG dari `balanceOf`, `inkOf`, `historyOf`.

## Cara pakai di project gw
Buat token komunitas: "holder card" soulbound otomatis, bisa dipakai buat allowlist/tiering (first-receipt order, never-emptied) tanpa snapshot off-chain.

## Caveat / jangan ditiru
- **Gas:** transfer pertama ke address baru = **290,679 gas** (fork test) vs 108k ke address lama. Kontrak yang deploy banyak vault/address baru (misal 1 vault per NFT) bayar ini tiap kali.
- Kontrak/pool juga kebagian NFT, jadi angka "holder" inflasi kalau tidak difilter.
- Soulbound bikin wallet gampang di-link (satu address = satu kartu publik).

## Bukti
- Fork mainnet (snapshot recon): `transfer` ke 2 address baru = 290,679 gas masing-masing, ke address lama 108,110
- Whitepaper jack.art/credits/whitepaper §4
