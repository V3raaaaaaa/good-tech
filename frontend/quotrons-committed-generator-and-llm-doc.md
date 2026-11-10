---
name: Koleksi bisa direproduksi dari seed + hash assignment di chain, plus satu file markdown buat ditanya ke AI
category: frontend
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [nft, provenance, reproducibility, docs, llm, transparency]
score: 7
status: claimed
added: 2026-11-11
source: recon 2026-11-11, app docs + quotrons.cash/quotrons-llm.md
---

# Koleksi bisa direproduksi dari seed + hash assignment di chain, plus file markdown buat AI

## Ringkas
1. **Provenance:** mesin mana, saham reward mana, dan art tiap ID ditetapin sebelum launch, terus hash file assignment-nya dikomit on-chain (`assignmentHash`). Generator + spec + audit likuiditas (yang milih 10 saham) dipublikasi. Siapa aja bisa jalanin ulang generator dengan seed yang sama, dapet koleksi yang persis byte-per-byte, hash, terus bandingin ke chain.
2. **Docs buat AI:** satu file `quotrons-llm.md` (~20 KB) yang isinya semua mekanik, pembagian fee, bobot tier, hash verifikasi, dan risiko. "Download, kasih ke ChatGPT/Claude, terus tanya apa aja."

## Kenapa bagus
- Gak ada "reveal" yang bisa dimainin tim. Assignment terkunci sebelum mint dan bisa dicek.
- File LLM = dokumentasi yang dibaca AI pengguna dengan benar, jadi jawabannya gak halusinasi. Cocok sama tren user nanya ke AI.
- Docs di app nyertain tabel error (tiap custom error + artinya + solusinya) dan event buat integrator.

## Cara pakai di project gw
Koleksi NFT/game: komit hash assignment sebelum mint + publikasiin generator dengan seed. Sediain `/<project>-llm.md` lengkap buat user dan agent.

## Caveat / jangan ditiru
- **Status `claimed`:** gw belum jalanin ulang generator (repo generator gak ketemu di akun GitHub publik pas recon). `assignmentHash` di chain udah dicek ada.
- File LLM harus di-update bareng app. Versi yang gw baca "Last updated 2026-08-13".

## Bukti
- `assignmentHash()` = `0xd385f0257ffb1ca15f9fb7bafba1896d1c0af0cc413d552e46145f1b36200fd0` di [0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F](https://robinhoodchain.blockscout.com/address/0x5a86828Efd322bfb16d93cFeD16EE9BC14940D7F?tab=contract)
- https://www.quotrons.cash/quotrons-llm.md
