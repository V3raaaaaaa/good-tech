---
name: Immutable UpgradeCap manager dengan timelock 48 jam per cap (Sui)
category: contracts
project: Blast (blast.fun)
chain: sui
tags: [upgrade, timelock, governance, move, custody]
score: 9
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://github.com/interest-protocol/blast-v2-contracts (sui/governance/upgrade_cap_manager), https://docs.blast.fun/developers/addresses/
---
# Immutable UpgradeCap manager dengan timelock 48 jam per cap (Sui)

## Ringkas
Shared object yang nyimpen `UpgradeCap` asli beberapa package di dalam `ObjectTable`. Controller (ManagerCap, dipegang multisig) cuma bisa *request* upgrade untuk digest persis atau request make-immutable. Request itu baru bisa dieksekusi 48 jam kemudian, dan yang ngeksekusi boleh **siapa aja**. Package manager-nya sendiri di-publish lalu langsung `make_immutable` di PTB yang sama, jadi aturannya nggak bisa diubah.

## Kenapa bagus
- Di Sui, UpgradeCap yang dipegang EOA/multisig = upgrade instan, user nggak punya waktu buat exit. Manager ini ngasih notice period yang ditegakkan on-chain tanpa harus percaya ke multisig.
- Digest dikunci waktu request, jadi kode yang di-deploy harus sama persis dengan yang diumumin 48 jam sebelumnya. Nggak bisa ganti bytecode diem-diem.
- "Anyone can execute" bikin multisig nggak bisa nahan-nahan (atau malah mempercepat) eksekusi. Satu request per cap, dan cap lain tetap independen.
- Manager-nya immutable, jadi trust-nya cuma ke ~430 baris kode yang bisa diaudit sekali aja.

## Cara kerja
- `new(cap)` → `(UpgradeCapManager, ManagerCap)`, terus `share`. `add_upgrade_cap` buat enroll cap lain (maks 256). Cap milik package manager sendiri ditolak (`ESelfEnrollment`).
- `request_upgrade(digest)` / `request_make_immutable` nyimpen `Request{action, ready_at_ms = now + 172_800_000}` sebagai dynamic field dengan key ID cap. Kalau masih ada request pending: `ERequestPending`.
- `authorize_upgrade(cap_id, clock)` (siapa aja) ngecek `now >= ready_at_ms`, hapus request, lalu `cap.authorize(policy, digest)` → `UpgradeTicket`. Publish upgrade, terus `commit_upgrade(receipt)` di PTB yang sama.
- `make_immutable` (siapa aja, setelah matang) ngeluarin cap dari tabel dan destroy.
- `cancel_request` cuma bisa dipanggil controller.
- ManagerCap cuma `key` (tanpa `store`), jadi nggak bisa di-wrap/share/freeze, cuma bisa dipindah lewat `transfer_cap`.

## Cara pakai di project gw
- Project Sui mana pun: publish manager (atau tulis versi sendiri, file ini MIT), enroll UpgradeCap semua package di tx pertama, kasih ManagerCap ke multisig.
- Bikin bot/watcher yang subscribe event `UpgradeRequested` terus ngumumin digest + link source, biar user sempet exit.
- Konsep yang sama bisa dipindah ke EVM: proxy admin = kontrak timelock immutable yang ngunci `keccak(newImpl.code)` waktu schedule.

## Caveat / jangan ditiru
- Delay di-hardcode 48 jam (const). Kalau lu butuh delay yang bisa diatur, perubahan delay-nya juga harus kena delay (lihat pola delayed-settings).
- Manager nggak nge-freeze object aplikasi. Make-immutable cuma matiin upgrade.
- Verifikasi sendiri bahwa UpgradeCap manager udah bener-bener di-destroy waktu publish (efek tx) **sebelum** enroll cap yang berharga.
- Kebanyakan modul Blast lain BUSL-1.1. File manager ini sendiri header-nya MIT.

## Bukti
- Source: https://github.com/interest-protocol/blast-v2-contracts/blob/main/sui/governance/upgrade_cap_manager/sources/blast_upgrade_cap_manager.move
- Publish + `0x2::package::make_immutable` dalam satu PTB: tx `8mJd2ph8DZWZ5J4UgWXrHjMTrm8V91dWJ3bDTzrqNqzS` (https://suiscan.xyz/mainnet/tx/8mJd2ph8DZWZ5J4UgWXrHjMTrm8V91dWJ3bDTzrqNqzS); package `0x6a00f462d690add7632ab159280474c3e2176c05e42f3494e37ce451de472958`
- Manager shared `0x33ec87fcf63be41e2ce0c608f2ab5462adf7c22f742629206b873144d56ef3e8` nyimpen 4 UpgradeCap (admin, partners, core, adapter Aftermath); ManagerCap `0x79d9a5a4ae50b5239cd0eefcd0ea54f0bb20531a568fa534bb2a4d56f8d91b60` dipegang multisig `0x818d6d70…d0a2` (Sui GraphQL, 2026-11-11)
- Docs: https://docs.blast.fun/developers/addresses/
