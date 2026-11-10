---
name: Admin hub contract (owner router + scoped pauser role)
category: security
project: Yield Fields
chain: Robinhood Chain (4663)
tags: [access-control, multisig, pause, solady, ownable-roles]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, YFOwnable 0x93F0494aF1d071D85b31eE41f6EbA51a2C52dbae + Safe 0x313a7ddC27D2329D27c6131BEF3dcFe6C6D9742A (Robinhood Chain)
---
# Admin hub contract (owner router + scoped pauser role)

## Ringkas
Semua kontrak game (staking, items, nanti pool/market) di-own oleh **satu** kontrak kecil "YFOwnable". Owner hub = Safe 2-of-3. Hub cuma punya dua jalur: `execute(target, data)` buat owner (semua admin call), dan `pause(target)` / `unpause(target)` buat holder `PAUSER_ROLE` (hot key ops).

## Kenapa bagus
- Ganti owner semua kontrak cukup satu `transferOwnership` di hub, nggak perlu N tx.
- Hot key buat incident response cuma bisa pause/unpause, nggak bisa ganti fee, upgrade, atau narik dana. Kerusakan kalau key bocor kebatas.
- Semua admin action lewat satu address, jadi gampang dimonitor (cukup watch tx ke hub + event Safe).

## Cara kerja
- Selector hub (diekstrak dari bytecode 2,027 B): `execute(address,bytes)`, `pause(address)`, `unpause(address)`, `PAUSER_ROLE()=1`, plus Solady OwnableRoles (`grantRoles`, `revokeRoles`, `rolesOf`, 2-step `requestOwnershipHandover`/`completeOwnershipHandover`).
- Kontrak target cuma ngecek `msg.sender == owner()`; `pause(target)` di hub manggil `target.setPaused(true)`.
- Simulasi `eth_call`: `execute(staking, setStructureFees(...))` dari Safe sukses, dari pauser EOA `Unauthorized()`; `pause(staking)` dari pauser sukses, dari address random `Unauthorized()`; `setPaused` langsung ke staking dari pauser `Unauthorized()`.

## Cara pakai di project gw
- Deploy hub dengan owner = Safe, grant `PAUSER_ROLE` ke 1–3 key ops / bot monitoring.
- Semua kontrak baru `initialize(owner_ = hub)`.
- Tambahin timelock di jalur `execute` buat aksi berbahaya (upgrade, fee), dan biarin `pause` instan.

## Caveat / jangan ditiru
- Di sini pauser juga bisa **unpause** (staking dibuka oleh EOA pauser, tx 0x7966d9dab0ee96579c1b9e361a06ecf3d29d3eeb1343c7676d0e2a735a8fdf54). Lebih aman: pause = hot key, unpause = multisig.
- `execute` tanpa timelock = Safe bisa upgrade UUPS instan.
- Hub sendiri nggak verified di explorer; fungsi disimpulkan dari selector.

## Bukti
- `owner()` staking 0x0AcFcD1483686fcd94DABeA03714321d0E05fc8D dan items 0xd9d6d0557F3479e801a967eb693ebE1ADA6E5317 = 0x93F0494aF1d071D85b31eE41f6EbA51a2C52dbae; `owner()` hub = Safe 0x313a7ddC27D2329D27c6131BEF3dcFe6C6D9742A (threshold 2, 3 owner).
- Grant role: Safe tx 0x044e9be81f2c75ef3abb8d123b6eb426bd3ff6a6414ea4247cd47bf37af0ad8b dan multiSend 0x78b2de65eead90dacc9c15a65de2e1f2d5b04412cf11645925b8d4288e8e4301.
