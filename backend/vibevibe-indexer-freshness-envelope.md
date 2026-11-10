---
name: Respons API indexer yang jujur soal freshness (asOfBlock + lag + coverage)
category: backend
project: vibe/vibe (Seedify)
chain: Robinhood Chain Testnet 46630
tags: [indexer, api-design, freshness, pagination, reorg]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, snapshot recon
---

# Respons API indexer yang jujur soal freshness (asOfBlock + lag + coverage)

## Ringkas
Tiap respons API bawa "amplop" yang bilang data ini dari block berapa (plus hash-nya), ketinggalan berapa block dari head, cakupan index-nya mulai dari mana, dan lengkap atau nggak. Frontend bisa nampilin "data basi" dengan jujur, dan cursor pagination ngunci snapshot block.

## Kenapa bagus
- User/bot tahu persis seberapa baru angkanya (`lagBlocks: 4`), bukan nebak.
- `asOfBlockHash` = bisa deteksi reorg: kalau hash beda dengan chain, data dibuang.
- `coverageStartsAtBlock` + `coverageComplete` = leaderboard/analytics gak diem-diem ngitung data separuh.
- Cursor pagination isinya `snapshotBlock` + `snapshotBlockHash` + filter hash + posisi terakhir, ditandatangan, jadi halaman 2 gak geser kalau ada data baru masuk.
- Error kode yang jelas dan bisa dibaca mesin (`SEASON_BOARD_OFF`, `TRADERS_BOARD_RETIRED` + pointer ke endpoint penggantinya).
- `config.freshnessPolicy` (`maxWriteLagBlocks`, `displayStaleAfterSeconds`) ngatur kapan UI matiin tombol write.
- Analytics punya `projection.revision` + `sha256` = hasil agregat bisa diverifikasi ulang.

## Cara kerja
```json
"meta": {"freshness": {"status":"FRESH","source":"INDEXER","asOfBlock":"151477487","asOfBlockHash":"0x7658…",
  "chainHeadBlock":"151477491","lagBlocks":"4","coverageStartsAtBlock":"91563904","coverageComplete":true}}
"page": {"limit":50,"hasMore":true,"nextCursor":"<base64 {snapshotBlock, snapshotBlockHash, sort, last{block,logIndex,token}}>.<hmac>"}
```

## Cara pakai di project gw
Wajib buat Mint Radar atau dashboard apapun yang baca chain: tambahin `asOfBlock/hash/lag/coverage` ke tiap respons, kunci pagination ke snapshot block, dan kasih UI aturan "stale setelah N detik". Ini juga nangkep kasus RPC yang diem-diem balikin kosong (pelajaran di [mintradar-recipe-replay-state-override](../data/mintradar-recipe-replay-state-override.md)).

## Caveat / jangan ditiru
- Nambah ukuran respons dan kompleksitas. Buat endpoint kecil/internal mungkin overkill.
- Snapshot cursor butuh query "as of block", jadi skema DB harus nyimpen block number di tiap baris.

## Bukti
- `GET https://testnet.vibevibe.fun/api/v1/chains/46630/v6/launches?limit=50` → `meta.freshness`, `data.page.nextCursor`
- `GET /api/v1/chains/46630/config` → `freshnessPolicy`; `/analytics/summary` → `projection.sha256`
