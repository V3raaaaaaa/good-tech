---
name: Creator rights buat akun sosial lewat account commitment + attestation backend
category: contracts
project: Blast (blast.fun)
chain: sui
tags: [creator-fees, attestation, ed25519, domain-separation, social-login]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://github.com/interest-protocol/blast-v2-contracts (sui/launch/launchpad/sources/launch/creator_authority.move), https://docs.blast.fun/launchpad/safety/
---
# Creator rights buat akun sosial lewat account commitment + attestation backend

## Ringkas
Penerima creator rights sebuah launch bisa berupa `Address(addr)` atau `Account(commitment)`, di mana commitment = hash 32 byte dari identitas off-chain (misal akun X). Pemilik akun belakangan nge-claim: backend nandatangani `domain || bcs({meme_type, account_commitment, claimant, expiry_ms})` pakai ed25519, kontrak verifikasi ke daftar public key signer, terus nerbitin `CurveFeeCap` + `CreatorMetadataCap` ke claimant.

## Kenapa bagus
- Coin bisa di-launch "untuk" seseorang yang belum punya wallet, dan fee-nya nunggu sampai orang itu login dan claim. On-chain cuma nyimpen hash, bukan handle mentah.
- Domain prefix `blast_fun::creator_claim::v1` + tipe coin (`type_name::with_original_ids<Meme>()`) di dalam message: signature nggak bisa di-replay ke launch lain atau ke message lain yang bentuk BCS-nya sama.
- `claimant` diikat ke `ctx.sender()` + ada expiry, jadi attestation curian nggak bisa dipake address lain.
- Signer disimpan di set on-chain dengan notice buat nambah, tapi revoke instan (signer bocor bisa langsung dimatiin dan semua attestation yang belum dipake ikut batal).
- Claim cuma sekali. Cap yang diganti admin otomatis invalid (launch cuma ngehormatin ID cap yang dia catat).

## Cara kerja
- `new_account(commitment)` (panjang dicek), simpan sebagai recipient waktu create.
- `claim_creator_caps(attestation)`: `peel_u64(expiry)`, `peel_vec_u8(sig)`, assert `now <= expiry`, rakit message, `signer_public_keys.any!(|k| ed25519_verify(sig, k, msg))`, lalu issue 2 cap.
- Cap terpisah: fee vs metadata. Masing-masing bisa di-destroy atau diganti admin dengan notice.

## Cara pakai di project gw
- Launchpad/creator-coin: "tag @handle", fee masuk escrow per commitment = `blake2b(provider || user_id || salt)`. Backend OAuth nerbitin attestation `(commitment, claimant, expiry)` dengan domain sendiri.
- EVM: EIP-712 dengan `chainId`, `verifyingContract`, `token`, `commitment`, `claimant`, `deadline`, plus set signer yang bisa di-revoke.

## Caveat / jangan ditiru
- Trust model-nya: backend signer bisa ngasih creator caps launch "Account" ke siapa aja. Kalau key bocor, fee creator bisa dicuri sampai di-revoke. Simpan di HSM/KMS dan pantau event claim.
- Commitment harus di-salt atau dibikin unik per provider. Kalau cuma hash user_id polos, gampang di-enumerate.
- BUSL-1.1, jadi tiru desainnya aja.

## Bukti
- Source: https://github.com/interest-protocol/blast-v2-contracts/blob/main/sui/launch/launchpad/sources/launch/creator_authority.move
- On-chain RuntimeConfig `0xc0b25b6adc2186c116d5bfa6442194c6cdb09eecc6c6907e98c737662b2c97f1` field `creator_claim_signers` berisi 1 public key, `delay_ms 172800000` (Sui GraphQL 2026-11-11)
- Docs: https://docs.blast.fun/launchpad/safety/ (baris "Claim-signer administrator")
