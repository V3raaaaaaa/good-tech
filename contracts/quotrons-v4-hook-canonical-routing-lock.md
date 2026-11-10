---
name: Kunci token ke satu pool V4 kanonik: otorisasi transient per arah + ban venue lewat codehash
category: contracts
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [uniswap-v4, hook, fee-enforcement, transient-storage, venue-lock, erc404]
score: 9
status: verified
added: 2026-11-11
source: recon 2026-11-11, source verified (Sourcify exact_match)
---

# Kunci token ke satu pool V4 kanonik: otorisasi transient per arah + ban venue lewat codehash

## Ringkas
Token cuma mau pindah dari/ke PoolManager Uniswap V4 kalau transfernya diotorisasi router kanonik untuk pool yang terdaftar di hook, dengan arah (masuk/keluar) dan jumlah persis, dan otorisasinya disimpan di **transient storage** yang harus habis dipakai di tx yang sama. Pool tipe V2/V3 (yang gak lewat PoolManager) diblokir pakai **runtime codehash**, jadi cuma kontrak yang bisa di-ban, wallet biasa (EOA) gak pernah.

## Kenapa bagus
- **Fee gak bisa dihindarin.** Satu-satunya jalan trading = pool kanonik yang hook-nya motong 3%. Fee ditegakkan token itu sendiri, bukan website.
- Slot transient terpisah buat masuk/keluar = gak bisa salah arah atau dipakai ulang. Ada `assertPoolTransferAuthorizationConsumed` buat ngecek otorisasinya habis.
- Ban pakai codehash cuma bisa kena kode kontrak (`require(codehash != keccak256(""))`), jadi transfer wallet ke wallet gak pernah bisa diblok.
- Router kanonik immutable, publik, tanpa API key. Bot/aggregator bisa langsung integrasi.
- Pelajaran dari V1: V1 gak ngikat PoolManager ke satu pool, jadi pool gak resmi tetap jalan (41% volume lewat pool tanpa fee, sampai $181.8k fee hilang).

## Cara kerja
```solidity
router.swap -> token.authorizePoolTransfer(dir, amount)          // tstore per arah
PoolManager settle/take -> token._transfer: require(tload(dir) == amount && pool == registered) ; tstore(dir, 0)
token.assertPoolTransferAuthorizationConsumed()                    // di akhir, harus 0
banVenueCodehash(hash, true)  // onlyOwner, hash != 0 && != keccak256("")
```

## Cara pakai di project gw
Token dengan fee/tax (launchpad, game token) yang mau fee-nya gak bisa diakalin: kunci transfer ke PoolManager lewat otorisasi transient dari router sendiri, terus blok pool lain berdasarkan codehash (bukan address, biar deploy ulang tetap kena).

## Caveat / jangan ditiru
- Ban codehash dipegang owner (EOA). Owner bisa ban venue apa aja yang berupa kontrak, termasuk wallet smart contract kalau codehash-nya cocok.
- Pas ban pool gak resmi, sisi token di pool itu **dibekukan** dan cuma admin yang bisa balikin. Itu nyakitin LP yang telat tahu.
- Token gak bisa dipakai di DEX/aggregator lain. Likuiditas cuma di satu tempat.
- Butuh EVM yang support transient storage (Cancun, EIP-1153).

## Bukti
- Token: [0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F](https://robinhoodchain.blockscout.com/address/0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F?tab=contract) (`authorizePoolTransfer`, `assertPoolTransferAuthorizationConsumed`, `banVenueCodehash`, `configurePoolRouting`)
- Hook: [0x62E200Cc8e4D95cf622f40Dd70f407C883EcB0cc](https://robinhoodchain.blockscout.com/address/0x62E200Cc8e4D95cf622f40Dd70f407C883EcB0cc?tab=contract) (`registeredPool`, `canonicalRouter`)
- [Post-mortem: canonical pools & external pools](https://github.com/mavrkofficial/quotrons-v1-post-mortem)
