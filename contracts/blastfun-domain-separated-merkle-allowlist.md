---
name: Merkle allowlist dengan domain separation, index di leaf dan cap per wallet
category: contracts
project: Blast (blast.fun)
chain: sui
tags: [merkle, allowlist, presale, blake2b, second-preimage]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://docs.blast.fun/developers/allowlists/, https://github.com/interest-protocol/blast-v2-contracts (sui/launch/core/sources/merkle.move)
---
# Merkle allowlist dengan domain separation, index di leaf dan cap per wallet

## Ringkas
Leaf = `blake2b256(0x00 || "blast-presale-v1" || bcs(index u64) || bcs(wallet) || bcs(cap u64))`, node = `blake2b256(0x01 || left || right)`. Arah hash ditentuin dari bit `index`, bukan dari sorting. Panjang proof harus persis `ceil(log2(leaf_count))`, dan wallet di leaf harus sama dengan sender.

## Kenapa bagus
- Prefix 0x00/0x01 nutup second-preimage attack (node internal disamarin jadi leaf). Banyak implementasi "sorted pair" OpenZeppelin-style lupa soal ini.
- Ada tag versi di leaf (`blast-presale-v1`), jadi tree buat produk/versi lain nggak bisa ketuker.
- `index` + `leaf_count` di-commit. Proof panjangnya fix, dan index harus `< leaf_count`, jadi nggak ada leaf palsu di luar tree.
- Cap per wallet ada di leaf (bisa tier/custom), dan commit berikutnya wajib nunjukin cap yang sama.
- Docs ngasih builder TypeScript lengkap (`@noble/hashes` + BCS `@mysten/sui`), aturan unpaired node-nya juga (dipasangin sama dirinya sendiri).

## Cara kerja
- Kontrak: `i = index`; buat tiap sibling, kalau `i` genap `node(digest, sib)`, kalau ganjil `node(sib, digest)`; `i /= 2`; hasil akhir harus sama dengan root.
- Sale nyimpen `allowlisted_eligibility(root, leaf_count)`. App nyajiin `(index, cap, proof)` per wallet.
- Commit selalu dikreditin ke `ctx.sender()`, jadi sponsored gas tetap aman (user tetap sender).

## Cara pakai di project gw
- Allowlist mint/presale/airdrop di chain mana pun: ganti hash ke keccak di EVM, tetap pakai prefix byte + tag versi + index + amount.
- Simpan `leaf_count` on-chain biar panjang proof bisa dicek.

## Caveat / jangan ditiru
- Leaf yang nyantumin index artinya urutan list harus deterministik dan dipublikasi. Ubah urutan = root baru.
- "Unpaired node pair with itself" itu keputusan builder. Kontrak nerima sibling apa adanya. Kalau tree builder lu beda, pastiin konsisten.
- Kode Blast BUSL-1.1. Skema hash-nya didokumentasiin publik, implementasiin sendiri.

## Bukti
- Spesifikasi + builder TS: https://docs.blast.fun/developers/allowlists/
- Source: https://github.com/interest-protocol/blast-v2-contracts/blob/main/sui/launch/core/sources/merkle.move
- Commit allowlisted: https://docs.blast.fun/developers/commit/
