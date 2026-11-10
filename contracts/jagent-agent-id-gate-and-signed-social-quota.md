---
name: Mint di-gate identitas on-chain (registrar Agent ID) + quota sosial pakai tanda tangan EIP-712 server, 1 akun sosial = 1 ID
category: contracts
project: $JAGENT (jager.live)
chain: BNB Smart Chain 56
tags: [sybil-resistance, identity, eip712, quota, social-tasks, referral]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, source verified
---

# Mint di-gate identitas on-chain + quota sosial pakai tanda tangan EIP-712

## Ringkas
Kontrak mint baca registrar `.ai` Agent ID (Binance Agentic Wallet) langsung on-chain: `handleOf(wallet)` → `id = keccak(handle)` → `ownerOf(id) == wallet`. Quota dihitung **per Agent ID** (bukan per wallet): 10 dasar, +1 per invitee yang mint pertama (dicatat on-chain pas mint), +1 per task sosial. Task sosial (follow, tweet, Telegram) dibuktiin pakai tanda tangan EIP-712 dari `quotaSigner` server, dan tiap akun sosial (`bytes32 account`) cuma bisa ngasih quota ke satu Agent ID (`accountAgent`).

## Kenapa bagus
- Gate identitas tanpa backend buat bagian intinya. Kontrak sendiri yang ngecek kepemilikan ID.
- Pindah wallet gak nambah quota, karena quota nempel di ID.
- Invite dicatat on-chain di mint pertama yang bayar, jadi gak bisa invite diri sendiri (`rid == id` ditolak).
- Tanda tangan server pakai domain (`JagentMint`, chainId, address kontrak) + deadline, jadi gak bisa di-replay di chain/kontrak lain.
- Satu akun X/Telegram gak bisa dipakai buat banyak ID.

## Cara pakai di project gw
Mint/WL yang butuh gate: baca registrar identitas on-chain di kontrak, simpan quota per identitas, dan bukti task off-chain lewat EIP-712 bertanda tangan server dengan binding akun sosial ↔ identitas.

## Caveat / jangan ditiru
- **Studio tetap menang:** satu operator bisa pegang ratusan Agent ID (leaderboard ambassador: 360 dan 318 invitee per orang). Gate identitas cuma naikin biaya per akun, gak nyegah farm.
- `quotaSigner` = key server yang bisa ngasih quota ekstra. Kalau bocor, quota bisa dicetak (tapi tetap bayar harga mint).
- Bergantung ke satu registrar pihak ketiga.

## Bukti
- Mint [0x3643A907f875fA9B740e1C0747E91b5aA5222aB8](https://bscscan.com/address/0x3643A907f875fA9B740e1C0747E91b5aA5222aB8#code): `_agent()`, `claimSocial()`, `_creditInvite()`, `accountAgent`, `socialDone`
