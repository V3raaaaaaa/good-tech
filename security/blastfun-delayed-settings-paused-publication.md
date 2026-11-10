---
name: Delayed settings on-chain + publish dalam keadaan paused
category: security
project: Blast (blast.fun)
chain: sui
tags: [timelock, admin, pause, governance, rbac, move]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://github.com/interest-protocol/blast-v2-contracts (sui/governance/admin), https://docs.blast.fun/security/
---
# Delayed settings on-chain + publish dalam keadaan paused

## Ringkas
Setiap parameter yang sensitif (fee, treasury, venue, signer, split vault, upgrade) disimpan sebagai objek "delayed": `{value, delay_ms, pending{value, ready_at_ms}}`. Admin cuma bisa *schedule*. Setelah matang, siapa aja boleh *apply*. Delay itu sendiri cuma bisa diganti lewat proposal yang tunduk ke delay **lama**. Package baru lahir dengan semua pause bit nyala, dan unpause ditolak selama delay upgrade masih bisa nol.

## Kenapa bagus
- Timelock-nya per setting, bukan satu timelock global, jadi lu bisa beda-bedain: SuperAdmin 7 hari, fee 48 jam, reward round 2 jam.
- "Ganti delay pakai delay lama" nutup trik klasik: turunin delay ke 0 dulu, baru ganti fee.
- RBAC pakai type: `AdminWitness<Role>` hasil `sign_in<Role>` di PTB yang sama, dan role di-parameterize per package (`PauseAdmin<OTW>`). Grant/revoke kelihatan sebagai event.
- Pause dipisah per bit (create/commit/migrate). Pause cuma nge-blok aksi baru; settlement, refund dan claim user tetap jalan.
- Publish ≠ aktif. Ini ngindarin window "baru deploy, config belum bener, udah ada yang pake".

## Cara kerja
- `delayed`, `delayed_set`, `delayed_map`, `delayed_action` di `sui/governance/admin/sources/delayed/`.
- `package_admin::wrap` makan `Publication<OTW>` + UpgradeCap fresh, lalu share `PackageVersion` (paused penuh) dan `PackageAdmin` (delay upgrade awal 48 jam).
- `clear_pause_bits` butuh `UnpauseAdmin<OTW>`, witness milik package itu sendiri (cuma kode package-nya yang bisa bikin), dan `upgrade.is_guarded()`.
- Version gate: `assert_current(version)` di tiap entry, jadi bytecode lama otomatis mati setelah upgrade (`commit_upgrade_and_advance` atomik).

## Cara pakai di project gw
- EVM: struct `Delayed{value, delay, pendingValue, readyAt, pendingDelay}` per parameter. `schedule()` onlyRole, `apply()` public. `scheduleDelay()` dihitung pakai delay sekarang.
- Deploy semua kontrak dalam keadaan `paused`, config, naikin delay, baru unpause. Jadiin itu checklist release.
- Watcher off-chain: diff field `pending` tiap N menit, kirim alert ke komunitas.

## Caveat / jangan ditiru
- Unpause di sini **instan**. Di deployment Blast, UnpauseAdmin juga dikasih ke dua key tunggal, jadi gate "paused sampai audit" bisa dibuka 1 key. Kalau lu niru, taruh unpause di multisig atau kasih delay juga, dan cuma pause yang boleh di key cepat.
- Dokumentasiin semua pemegang role. Daftar role on-chain Blast lebih banyak dari yang ditulis di docs.
- Kode Blast BUSL-1.1. Tiru polanya aja.

## Bukti
- Source: https://github.com/interest-protocol/blast-v2-contracts/tree/main/sui/governance/admin/sources
- On-chain (Sui GraphQL 2026-11-11): Treasury `0x11f54f5cabdf5f1add9b05d54229dee53a16f698e08016aae8a6068b9f281b7e` `destination.delay_ms = 172800000`; ACL `0xec294e9b3ce0a0ffb123ab1a90dfedd2a368f20744e95c368726283c81e62f52` `super_admin_transfer.delay_ms = 604800000`; PackageVersion launchpad `0x25b905a97e1c4e66be7b332e0d4e4b37a423f7cfb1dbdbe6e088e561df7d0ee3` `paused = 7`
- Drill unpause→pause dalam 1 PTB: tx `GR43kRCrzBCMqauZMAtRK2rg3wfw8U6ad3mTGpQNY7oz` (https://suiscan.xyz/mainnet/tx/GR43kRCrzBCMqauZMAtRK2rg3wfw8U6ad3mTGpQNY7oz)
- Docs: https://docs.blast.fun/security/
