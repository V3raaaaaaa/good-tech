---
name: Sync game pakai intent + claim, ledger ekonomi di server, txid idempotent + versi
category: backend
project: SINDICAT
chain: -
tags: [game, server-authoritative, anti-cheat, sync, idempotency, optimistic-concurrency]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, laporan recon internal
---

# Sync game pakai intent + claim, ledger ekonomi di server, txid idempotent + versi

## Ringkas
Client tetap simulasi game secara lokal (biar responsif), tapi yang dikirim ke server bukan hasil, melainkan **niat** ("jual 10 catnip", "mulai batch rig") dan **klaim** ("pot 3 udah matang, gw panen"), bareng save lokal, `txid` unik, dan `baseVersion`. Server ngecek klaim ke timer/state dia sendiri, ngitung hasilnya, terus balikin doc + uang + inventory + gear + market versi ledger server. Client mengimpor itu dan buang versinya sendiri.

## Kenapa bagus
- **Game modif gak bisa bikin apa-apa.** Uang, item, dan market dihitung ulang server ("argent recalé sur le serveur"). Klaim yang gak sesuai ditolak `422 implausible`.
- **Tetap terasa lokal/instan.** Client gak nunggu server buat tiap gerakan, cuma rekonsiliasi per batch aksi.
- **`txid` UUID = idempotent.** Retry karena jaringan putus gak dobel kredit.
- **`baseVersion` + `409` dengan doc server = optimistic concurrency.** Dua device gak bisa saling timpa, dan server menang.
- **RNG di-seed dari txid** (`rngBase`), jadi loot/hasil acak bisa direproduksi dan diverifikasi server.
- Status error yang jelas: `401` (session), `403 banned/waitlisted`, `409 conflict`, `422 implausible`, `429 too_many_accounts`.
- Batch intents + claims dikirim juga pas tab ditutup (`keepalive` kalau < 60 KB).

## Cara kerja
```
POST /api/act      {txid, baseVersion, doc, action}
POST /api/intents  {txid, baseVersion, doc, claims:[...], intents:[{...,at}]}
  200 -> {ok, version, doc?, result(s), inv, gear, market, money, xp, mailbox, replay}
         client.import(doc, {rngBase: hash(txid)})
  409 -> {doc, version}  (server menang, client adopsi)
  422 -> {why}           (klaim/save gak masuk akal)
PUT  /api/state    {doc, baseVersion}  -> server timpa money/inv/gear/market dari ledger
```

## Cara pakai di project gw
Buat game web apapun yang punya ekonomi bernilai (mini game, P2E, quest): client simulasi, server simpan ledger. Kirim intent + claim bertimestamp, server cek "boleh gak" + "udah waktunya gak", terus kirim balik state final. Selalu pakai txid + version.

## Caveat / jangan ditiru
- Kompleks: dua implementasi aturan (client buat preview, server buat kebenaran) harus sinkron, kalau nggak, pemain sering kena "refused".
- Combat real-time (Colyseus) itu masalah lain: perlu server simulasi atau validasi input. Pola ini cocok buat ekonomi/crafting/timer.
- Server SINDICAT closed source. Yang terbukti cuma kontrak client↔server-nya.

## Bukti
- `game.js` (snapshot recon): `actNow`, `intentsNow`, `pushStateNow`, `fetchState`, `adoptEmptyServer`, `runImport(...{rngBase:e2(u)})`
