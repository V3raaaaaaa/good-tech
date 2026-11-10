---
name: Launch dengan finalisasi satu arah: fee launch 90% anti-sniper → 3% permanen, semua fungsi setup terkunci
category: contracts
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [launch, anti-snipe, finalization, setup-lock, admin-minimization]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, source verified + eth_call
---

# Launch dengan finalisasi satu arah

## Ringkas
Kontrak dideploy dalam mode setup (`transfersLocked = true`). Semua fungsi konfigurasi (`setReflections`, `configurePoolRouting`, `configureMigration`, `configureEmergencyControls`, `setRoyaltyReceiver`, `setExempt`, `setSetupAllowed`) cuma bisa dipanggil sekali dan cuma sebelum launch, terus revert (`AlreadyLaunched` / `AlreadyConfigured`). Masa launch pakai **fee 90%** buat wallet di luar tier yang dipublikasi (anti-sniper/bot), terus `finalizeLaunchFees()` permanen nurunin ke 3% buat semua.

## Kenapa bagus
- Setelah launch, gak ada "setter" tersembunyi buat ngalihin reward, royalty, atau exemption.
- Preflight launch nolak izin setup yang belum dicabut (`setupAllowedCount` harus 0).
- `recoveryAdmin` wajib kontrak (`code.length > 0` = Safe), bukan EOA.
- Fee 90% bikin sniping di blok awal gak masuk akal, dan finalisasinya keliatan on-chain.
- Metadata bisa dibekukan permanen (`freezeMetadata`).

## Cara pakai di project gw
Token/koleksi apa pun: pisahin fase setup dan live dengan satu flag, semua setter wajib `require(!launched)` + sekali pakai, ada counter izin setup yang harus 0, dan fee launch tinggi sementara yang finalisasinya satu arah.

## Caveat / jangan ditiru
- `setPaused` dan `banVenueCodehash` sengaja dibiarin hidup setelah launch (onlyOwner, tanpa timelock).
- Fee 90% bisa nyakitin pembeli biasa yang gak baca. Butuh UI yang teriak keras.

## Bukti
- Token [0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F](https://robinhoodchain.blockscout.com/address/0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F?tab=contract): `setupAllowedCount()`=0, `metadataFrozen()`=true, `emergencyControlsConfigured()`=true; hook `launchFeesFinalized()`=true
