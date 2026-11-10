---
name: Post-mortem insiden standar audit: label bukti, dual cutoff, Merkle alokasi, restitusi per event
category: security
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [incident-response, post-mortem, migration, merkle, restitution, transparency]
score: 9
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://github.com/mavrkofficial/quotrons-v1-post-mortem
---

# Post-mortem insiden standar audit

## Ringkas
Setelah exploit V1, tim bikin repo publik yang misahin narasi, ledger mesin, artefak snapshot mentah, dan script reproduksi. Tiap klaim dikasih label: **On-chain** (bisa diulang dari state/log), **Committed** (dicover block hash, Merkle root, SHA-256), **Derived** (dihitung deterministik), **Market-indexed** (bergantung index DexScreener), **Pending** (belum dieksekusi).

## Kenapa bagus
- **Dual cutoff** yang dijelasin alasannya: likuid dibekukan di block shutdown pool resmi, hardwired di block pengumuman, karena V1 gak punya global pause dan pool gak resmi masih bisa trading.
- **Merkle root alokasi** (4.307 leaf, 734 penerima), dan ID terminal hardwired dipertahanin persis (inverse index di pool).
- **Restitusi per event** (360), dengan peringatan eksplisit bahwa jumlah event ≠ ID unik ≠ korban unik.
- Bagian "What this report does not claim" + "tidak mengidentifikasi orang di balik address".
- Distribusi langsung ke wallet, user gak perlu klaim atau sign apa pun.
- Pembelian setelah cutoff (termasuk di OpenSea/pool gak resmi) gak dapet hak, dan aturannya ditulis sebelum distribusi.

## Cara pakai di project gw
Template buat kalau project lu kena insiden: repo terpisah dengan `docs/01-incident`, `02-migration`, `03-markets`, `04-v2`, `05-verification`, plus `data/*.csv|json`, `SHA256SUMS`, dan label bukti per klaim.

## Caveat / jangan ditiru
- Restitusi pakai recovery admin = butuh kuasa maksa mindahin aset. Kuasa itu sendiri jadi risiko permanen di V2.
- Status di README repo masih nulis distribusi "pending". Dokumen gak di-update setelah eksekusi (app bilang udah final).

## Bukti
- https://github.com/mavrkofficial/quotrons-v1-post-mortem (README, docs/, data/, SHA256SUMS, scripts/)
