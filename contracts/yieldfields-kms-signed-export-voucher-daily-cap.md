---
name: Off-chain → on-chain item export pakai voucher EIP-712 dari KMS signer + daily cap on-chain
category: contracts
project: Yield Fields
chain: Robinhood Chain (4663)
tags: [eip712, voucher, aws-kms, erc1155, blast-radius, game-items]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, Items 0xd9d6d0557F3479e801a967eb693ebE1ADA6E5317 (Robinhood Chain), https://yieldfields.fun/api/health, https://yieldfields.fun/docs/deed-gameplay/fertilizer
---
# Off-chain → on-chain item export pakai voucher EIP-712 dari KMS signer + daily cap on-chain

## Ringkas
Item game (Fertilizer) hidup off-chain di "Bag" (Postgres). Kalau user mau trade, server nge-sign **mint voucher EIP-712** pakai key di **AWS KMS**, user submit `mintOnChain(voucher, sig)` → dapet ERC-1155C. Import balik = `burnOffChain(ids, amounts)` → event `Imported` → server credit lagi ke Bag. Kontrak nge-cap jumlah mint per token id per hari secara global.

## Kenapa bagus
- Private key signer nggak pernah ada di env server (mode `kms`, keliatan di `/api/health`).
- Kalau signer tetap bocor, kerusakannya kebatas: `dailyCap(tokenId)` (60,000/hari) + replay guard `isUsed(requestId)` + field `player` di voucher (error `WrongPlayer`) + `Expired`.
- Game logic yang mahal (rate, limit per wallet, anti-farm) tetap di server, chain cuma jadi "bank" yang ngejaga invariant kasar.
- Import nggak butuh signature: burn on-chain dari wallet sendiri, server tinggal index event.

## Cara kerja
- Voucher (tuple, di-hash via `hashMintVoucher`): player, requestId, ids/amounts, deadline (disimpulkan dari ABI + error).
- `mintOnChain` cek sig == `signer()`, `!isUsed(requestId)`, `mintedToday(id)+amt <= dailyCap(id)`, emit `Exported(player, requestId)`.
- Rotasi signer: `setSigner` dari owner (Safe → admin hub). Signer awal EOA 0x6473…9f3c diganti ke KMS address 0x91C0d58FFA5e6ba5eA2e37C95684C5241e4FF660 (tx 0x51a009ba92adb6ed015e4b84e43e8495208d4132d415ec9271ef08a9136dfd8b).
- Env backend: `YF_MINTER_SIGNER_KMS_KEY_ID` dengan fallback `YF_MINTER_SIGNER_PRIVATE_KEY`, `AWS_ROLE_ARN` (IAM role, cocok sama Vercel OIDC federation).

## Cara pakai di project gw
- Pakai viem custom account yang nge-sign lewat KMS (`secp256k1` key spec `ECC_SECG_P256K1`), normalisasi `s` ke low-s dan cari `v` dengan recover.
- Tambahin `dailyCap` per id + `isUsed(requestId)` + `player` di struct. Set cap = beberapa kali volume normal.
- Expose `/api/health` yang ngasih signer address + mode (bukan key!) biar monitoring bisa alert kalau signer berubah.

## Caveat / jangan ditiru
- Owner di sini bisa `adminMintOnChain` tanpa cap (simulasi mint 1,000,000 dari owner sukses). Kalau mau trust, cap juga jalur admin atau hapus.
- Limit export per wallet cuma di-enforce server; user harus percaya backend.
- Kontrak UUPS tanpa timelock dan source belum verified.

## Bukti
- `signer()` = 0x91C0d58FFA5e6ba5eA2e37C95684C5241e4FF660 (EOA nonce 0), `defaultDailyCap()=60000`, `mintedToday(1)=1054`.
- https://yieldfields.fun/api/health → `"signerModes":{"minter":"kms"}`.
- 7,355 Fertilizer di-mint via export, 818 di-burn via import, 433 exporter (log TransferBatch/TransferSingle di 0xd9d6…5317).
