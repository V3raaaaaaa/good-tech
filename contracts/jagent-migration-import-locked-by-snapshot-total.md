---
name: Migrasi saldo ke kontrak baru yang dikunci total snapshot immutable (import cuma bisa ditutup kalau angkanya pas)
category: contracts
project: $JAGENT (jager.live)
chain: BNB Smart Chain 56
tags: [migration, snapshot, import, immutable, token-relaunch]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, source verified + eth_call
---

# Migrasi saldo ke kontrak baru yang dikunci total snapshot immutable

## Ringkas
Waktu pindah ke kontrak token/mint baru, saldo 1.161 holder lama (snapshot di blok 130.223.532) diimpor batch oleh `importer`. Total saldo snapshot ditanam sebagai **immutable** `snapshotTotal` waktu deploy. `lockImport()` cuma bisa jalan kalau `importedTotal == snapshotTotal`. Setelah dikunci, gak ada lagi yang bisa diimpor (`ImportClosed`). Quota, task sosial, dan jumlah share per Agent ID juga ikut diimpor dengan pola yang sama.

## Kenapa bagus
- Importer gak bisa nyelipin saldo ekstra buat dirinya sendiri: total harus pas sama angka yang dikomit sebelum import mulai.
- Mint/unpause baru bisa jalan setelah import dikunci (`setPaused(false)` butuh `importLocked`).
- Bisa dicek publik: `snapshotTotal()` == `importedTotal()` == `4.739e29`.

## Cara pakai di project gw
Relaunch/migrasi token: komit total snapshot (dan idealnya Merkle root) sebagai immutable di constructor, import batch, terus lock yang mensyaratkan total pas. Jangan buka fungsi utama sebelum lock.

## Caveat / jangan ditiru
- Total yang pas gak ngebuktiin **distribusinya** benar per holder. Pakai Merkle root kalau mau tiap leaf bisa diverifikasi (contoh lebih kuat: post-mortem QUOTRONS).
- Importer tetap satu key selama fase import.

## Bukti
- Mint [0x3643A907f875fA9B740e1C0747E91b5aA5222aB8](https://bscscan.com/address/0x3643A907f875fA9B740e1C0747E91b5aA5222aB8#code): `snapshotTotal()` = `importedTotal()` = 473943206354912496343831373276, `importLocked()` = true
