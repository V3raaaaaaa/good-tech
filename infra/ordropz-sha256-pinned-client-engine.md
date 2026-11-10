---
name: Client engine di-pin pakai sha256 + client-side vault
category: infra
project: Ord Dropz (shielded Ordinals launchpad)
chain: Bitcoin
tags: [supply-chain, integrity, esm, client-side, psbt]
score: 7
status: verified
added: 2026-11-11
source: Trollbox recon 2026-10-19
---

# Client engine di-pin pakai sha256 + client-side vault

## Ringkas
Semua transaction builder (mint, vault, signing PSBT) ada di satu ESM bundle yang di-load dari API, dan site nge-pin bundle itu pakai sha256. Vault sepenuhnya client-side.

## Kenapa bagus
- **Integrity pin**: kalau server/CDN dibobol dan engine diganti, hash gak cocok dan gak jalan. Ini proteksi supply-chain yang jarang dipakai project web3.
- Satu bundle 559 KB, ESM murni, jalan di Node 22 tanpa browser shim. Builder yang sama dipakai web dan bot, gak ada dua implementasi yang bisa beda.
- Export API bersih: `buildMint`, `vaultAddress`, `keyring`, `signVaultPsbt`, `walletFromSeed`.
- `buildMint` cuma butuh `view.cid`, gak perlu download state 5 MB.

## Cara kerja
Site fetch `<apiBase>/engine/shielded-browser.js`, cek sha256 vs hash yang di-hardcode, baru import. Vault seed diturunin dari signature wallet atas `VAULT_KEY_MESSAGE`.

## Cara pakai di project gw
Kalau project gw punya logic signing/tx builder di frontend: pisahin jadi satu engine module, publish dengan hash, dan pin hash-nya di app (atau pakai SRI `integrity=` di `<script>`). Bonus: bot/SDK pihak ketiga bisa pakai engine resmi, bukan reverse engineer.

## Caveat / jangan ditiru
- Vault seed dari signature itu konvensi, bukan dipaksa protokol: siapa pun bisa derive seed dari 32 byte mana aja. Jangan anggap itu bukti kepemilikan wallet.
- Repo open-source mereka bilang builder gak ada di repo, padahal bisa didownload. Klaim "closed" di docs ≠ kenyataan.
- Per-wallet cap dihitung per *address*, dan vault pakai address baru tiap mint, jadi cap-nya gak efektif.
- `STATUS.md` mereka: Groth16 spend key dari satu kontribusi lokal (trusted setup lemah).

## Bukti
- Engine: `<apiBase>/engine/shielded-browser.js`
- Repo: `Fl1ntstowned/shielded-ordinals`
- Kode: internal (gak di-share)
