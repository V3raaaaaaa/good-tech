---
name: Launch coin + fee split permanen dalam satu Jito bundle
category: contracts
project: forks.wiki
chain: Solana mainnet (pump.fun)
tags: [launchpad, pump-fun, fee-share, jito, bundle, github, non-custodial]
score: 9
status: verified
added: 2026-11-11
source: recon 2026-11-11, laporan recon internal
---

# Launch coin + fee split permanen dalam satu Jito bundle

## Ringkas
Coin pump.fun di-create bareng fee sharing config dan split final (admin di-revoke) dalam satu bundle Jito. Hasilnya: gak pernah ada momen coin udah live tapi split-nya belum ke-lock.

## Kenapa bagus
- **Atomik.** Create, config, dan lock masuk bareng atau gak masuk sama sekali. Gak ada celah dev ganti split abis launch.
- **Non-custodial dengan verifikasi.** Server bikin tx, wallet sign duluan, server cek `sha256(message)` sama persis dengan yang dibikin dan semua signature valid, baru mint keypair co-sign. Kalau wallet ngubah tx, ditolak.
- **Mint key cuma lewat.** Disimpan terenkripsi AES-256-GCM di ticket HMAC 150 detik, gak ada di DB.
- **Listing dari chain, bukan dari request.** Coin baru dianggap `live` setelah dibaca balik: creator curve == config PDA, shares sama, `adminRevoked`.
- Dev buy (opsional) ditaruh *setelah* lock, jadi fee dari buy pertama pun ikut ke split.

## Cara kerja
```
tx A  createSocialFeePda(userId, Platform.GitHub)     // kalau penerima GitHub belum punya akun fee
tx B  createV2Instruction + createFeeSharingConfig    // coin + creator vault pindah ke config
tx C  updateFeeSharesV2(current=[user], new=holders)  // split final, admin revoked
tx D  buyInstructions + fee transfer + Jito tip       // opsional
```
Tiap tx ≤ 1232 byte (dicek), tip Jito di tx terakhir, `sendBundle` retry 3x kalau 429. Penerima GitHub = `socialFeePda(String(githubId), Platform.GitHub)`, diklaim di pump.fun pakai login GitHub.

## Cara pakai di project gw
Pola ini cocok buat launchpad apapun yang janjiin "fee ke X dikunci": bikin semua tx di server dari state yang server tentuin, hash tiap message, kasih wallet sign, verifikasi hash + signature, baru co-sign dan kirim sebagai bundle. Di EVM padanannya: satu tx ke factory yang create + set split + renounce, atau multicall.

## Caveat / jangan ditiru
- Primitif fee GitHub/X punya pump.fun (dan Bags.fm), bukan buatan forks.wiki. Kalau pump.fun ganti program, flow ini ikut ganti.
- User tetap sign tx bikinan server. Server dibobol = tx bisa diganti; penangkalnya cuma simulasi wallet.
- Penerima fee masuk tanpa izin mereka (opt-out). Jangan launch atas nama orang tanpa persetujuan kalau mau aman secara reputasi/hukum.
- Repo publik ketinggalan dari versi live, jadi audit kode ≠ yang jalan.

## Bukti
- 27/27 coin: creator == fee config PDA, `adminRevoked = true`, 30% cocok ke PDA GitHub owner/top contributor (`onchain.json` (snapshot recon))
- Kode: [netlify/lib/chain.mjs](https://github.com/forkwiki/fork/blob/main/netlify/lib/chain.mjs), `netlify/functions/launch.mjs`
- Repo: https://github.com/forkwiki/fork
