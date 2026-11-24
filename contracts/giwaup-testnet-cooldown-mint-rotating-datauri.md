---
name: Testnet engagement NFT — cooldown mint + metadata data-URI dengan artwork rotasi
category: contracts
project: GIWA UP (giwaup.xyz)
chain: giwa-sepolia
tags: [erc721, testnet, cooldown, data-uri, onchain-metadata, engagement, pre-mainnet]
score: 5
status: verified
added: 2026-11-24
source: recon 2026-11-24, https://sepolia-explorer.giwa.io/address/0x5F1276Cd1De9f7078d67A877d646Ab3C108444eB, https://testnet.giwaup.xyz/
---
# Testnet engagement NFT — cooldown mint + metadata data-URI dengan artwork rotasi

## Ringkas
Kontrak ERC-721 kecil (7,8 KB) buat "pemanasan" sebelum mainnet chain-nya ada. Mint gratis, 1 per wallet tiap `cooldown` (12 jam), tanpa total cap. `tokenURI` balikin JSON base64 `data:` yang dirakit on-chain: nama `#id`, deskripsi, trait Era/Gender/Edition, dan `image` = `imageURLs[id % imageCount]`. Jadi 7 gambar dipakai ulang buat puluhan ribu token tanpa server metadata.

## Kenapa bagus
- Nol backend: gak ada API metadata yang bisa mati, gak ada reveal. Halaman mint-nya satu file HTML statis + ethers dari CDN.
- Cooldown per wallet (`lastMintAt` / `nextMintAt(address)`) bikin orang balik tiap 12 jam. Itu retensi yang murah, dan frontend tinggal baca `nextMintAt` buat countdown.
- Deskripsi kontrak nulis terang "no mainnet rights, no token allocation, no airdrop promise". Ekspektasi dikunci di metadata, bukan cuma di website.
- Tanpa fungsi payable dan tanpa withdraw: gak ada jalur uang yang perlu diaudit.

## Cara kerja
- Selector yang kebaca dari bytecode: `mint()`, `mint(uint256)`, `nextMintAt(address)`, `lastMintAt(address)`, `cooldown()`, `maxPerWallet()`, `imageCount()`, `imageURLs(uint256)`, `eras(uint256)`, `genders(uint256)`, `description()`, `externalURL()`.
- Owner: `setImage(uint256,string)`, `setDescription(string)`, `setCooldown(uint256)`, `setMaxPerWallet(uint256)`, `ownerMint(address,uint256)`, `ownerMintBatch(address[])`.
- `tokenURI(1)` → `{"name":"GIWA UP Testnet #1", ..., "image":"https://testnet.giwaup.xyz/img/1.jpg","attributes":[Era, Gender, Edition=Testnet]}`.

## Cara pakai di project gw
- Pakai buat kampanye testnet / pre-mainnet: satu kontrak, N gambar, cooldown. Tambahin event `Minted(address,uint256)` biar gampang di-index.
- Simpen gambar di IPFS/Arweave, bukan domain sendiri, kalau mau klaim "on-chain metadata" tetap jujur.
- Verifikasi source di explorer. Kontrak sekecil ini gak ada alasan buat unverified.

## Caveat / jangan ditiru
- Kontraknya **unverified**. Semua di atas dibaca dari selector + `eth_call`.
- `image` nunjuk ke domain project, dan owner bisa `setImage` kapan aja. Metadata-nya on-chain, gambarnya enggak.
- UI bilang "up to 50 per wallet", on-chain `maxPerWallet = 1.000.000` (di-set owner sehari setelah deploy). Batas yang beneran jalan cuma cooldown. Samain angka di UI dengan kontrak.
- `ownerMintBatch` dipakai buat ngirim 37.595 dari 49.360 token ke alamat orang lain. Lihat entry data soal holder count yang digelembungin.
- Owner = satu EOA, gak ada renounce.

## Bukti
- Kontrak: https://sepolia-explorer.giwa.io/address/0x5F1276Cd1De9f7078d67A877d646Ab3C108444eB (deploy 2026-10-30 10:32 UTC, tx `0x183a8f5de501a17d8e1a1675cdd1677d62b69890d5946e9cd2dcf1d3c019ded6`)
- `eth_call` 2026-11-24 via https://sepolia-rpc.giwa.io/ : `cooldown() = 43200`, `maxPerWallet() = 1000000`, `imageCount() = 7`, `totalSupply() = 49360`
- `setMaxPerWallet(1000000)` oleh deployer 2026-10-31 02:34 UTC (explorer, tab transaksi deployer `0xD77EB2b29E732B957655a4Df38f62a3fEFA00AAA`)
