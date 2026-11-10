---
name: Heat + laundering: risiko pegang cash dan exit token yang dipersempit lewat "front business"
category: tokenomics
project: SINDICAT
chain: Robinhood Chain (planned)
tags: [game-economy, outflow-control, emission, sink, lore-driven-design, p2e]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, `game.js` (snapshot recon) + codex.html
---

# Heat + laundering: risiko pegang cash dan exit token yang dipersempit lewat "front business"

## Ringkas
Mata uang game (SIN) bisa didapat dari 3 trade, tapi tiap SIN "kotor" naikin **HEAT**. Kalau heat penuh, polisi nangkep (penjara makan waktu dan bail kecil, gak ada yang disita). Uang bisa diamanin di bank, dibelanjain, atau dicuci lewat **front business** yang dibeli mahal dan punya kapasitas cuci per hari. **Satu-satunya jalan keluar ke wallet on-chain adalah lewat front**, sedangkan bank gak pernah ngirim ke wallet.

## Kenapa bagus
- **Rate limit outflow token yang nyatu sama lore.** "Cash out" dibatesin `outPerDay` per front + `launderMs` + cut boss 20%, jadi gak perlu aturan withdraw yang terasa dibuat-buat.
- **Front = sink besar** (buy cost sampai 50k SIN) yang sekaligus jadi syarat exit. Yang mau narik keluar harus investasi di dalam game dulu.
- **Heat beda per trade** (`heatPerSin`: catnip 0.009, data 0.06, fishing 0), jadi pemain milih profil risiko. Fishing (gak ada heat) = jalur aman tapi pelan.
- **Emisi global dibatasi:** `potPerDay` 1M SIN dibagi 3 ronde (00/08/16 UTC), dan `/api/pot` ngasih tau sisanya. Gak ada inflasi tak terbatas walau bot banyak.
- **Hukuman yang gak bikin trauma:** penjara = waktu, mati = sebagian barang + durability, SIN gak hilang. Pemain gak rage-quit.
- **Deposit dibatasi** 20k/hari + fee 1% dan harus disaksikan server, jadi gak ada "browser yang ngekredit dirinya sendiri".
- **Circuit breaker admin** buat nge-pause semua exit sekaligus pas ada exploit.

## Cara kerja
```js
Ei = { potPerDay: 1e6, perAccountPerDay: 1e6, rates: {catnip:{skunk:4,purplekush:8,criminalkush:15}, fish:{...}, data:1},
       heatPerSin: {catnip:.009, fish:0, data:.06} }
su = { perDay: 3 }                          // 3 ronde pot per hari UTC
fronts = { cafe:{tier, buyCost, outPerDay, launderMs:15min}, ..., casino:{buyCost:5e4, outPerDay:2e3} }
Ac = { bossCutPct: 20, bossEntryPct: 10 }
bail = 150..500 SIN + 2% cash (cap 500), dari cash dulu baru safe
```

## Cara pakai di project gw
Game dengan token: bikin "exit" token jadi mekanik game yang butuh investasi dan punya kapasitas harian (gudang, pelabuhan, bank cabang). Pasang risiko memegang mata uang (heat/pajak/raid NPC) biar pemain spend atau stake. Pool emisi global per ronde, bukan per pemain doang.

## Caveat / jangan ditiru
- Token mainnet SINDICAT belum ada, jadi mekanik exit belum diuji di dunia nyata.
- Circuit breaker = admin bisa ngunci semua uang keluar. Harus ada aturan publik kapan dipakai.
- `perAccountPerDay` = `potPerDay` (1M) artinya satu akun secara teori bisa ngabisin pool. Batas per akun mestinya jauh lebih kecil.
- Exit yang terlalu sempit bikin pemain merasa token "gak bisa dicairin" dan nilainya bisa jatuh.

## Bukti
- `game.js` (snapshot recon): konstanta `Ei`, `su`, `Ac`, objek front (`casino:{buyCost:5e4,outPerDay:2e3,launderMs:15*Lo}`), fungsi `Fx` (pot per ronde), `gd` (id ronde)
- `walletPanel-*.js`: "No way out here, ever: the bank never sends to your wallet. Your exit runs through your FRONTS." + cap 20 000/day, fee 1%
- `admin-*.js`: "Circuit breaker: pause or resume every facade exit (wallet / Hood Stock) for everyone"
