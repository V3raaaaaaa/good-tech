---
name: Deploy immutable per "run" + frontend pin runtime hash bytecode
category: infra
project: vibe/vibe (Seedify)
chain: Robinhood Chain Testnet 46630
tags: [deployment, immutable, versioning, integrity, frontend-config]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, `domain-shared-*.js` (snapshot recon) + /config
---

# Deploy immutable per "run" + frontend pin runtime hash bytecode

## Ringkas
Kontrak gak pakai proxy. Tiap versi baru di-deploy sebagai set kontrak baru ("run": run14, run15, run18, run19). Frontend nyimpen semua run beserta `deployBlock`, address, fitur, dan `runtimeHash` bytecode-nya. Token lama tetap kebaca dan bisa ditradingin di kontrak run-nya sendiri.

## Kenapa bagus
- **Gak ada upgrade diam-diam.** Aturan buat token yang udah di-launch gak bisa diubah setelahnya.
- **Integrity check:** frontend bisa bandingin `keccak(eth_getCode(addr))` dengan `runtimeHash` yang di-pin. Kalau beda (RPC bohong atau address ketuker), UI bisa nolak.
- **Feature flag per run** (`pairRewards`, `giftLists`, `openingWithheld`, `forcedOpeningBuy`…), jadi UI tahu kemampuan tiap generasi kontrak tanpa nebak.
- `deployBlock` per run bikin indexer tahu harus scan mulai dari mana.
- Satu env bisa nge-serve lebih dari satu run (`v6: {graph: "run19", alsoServes: ["run15"]}`), jadi migrasi pelan-pelan tanpa matiin yang lama.
- Config env (prod/staging/preview) di-seal pakai hash (`seal: "sha256:…"`).

## Cara kerja
```js
v6Graphs: {
  run19: { chainId: 46630, deployBlock: 149342359, factory, zap, hook, locker, buyback, pairPolicy, giftLists,
           pairs: [...], launchZero: {...}, features: { pairRewards: true, giftLists: true, openingWithheld: true } },
  run15: { ... }, S3: { run: "run18", ... }
}
legacyPublicGraphs: [{ factory, hook, ..., runtimeHashes: { factory: "0xde5e…", hook: "0x4583…" } }]
env: { origins: [...], api: "same-origin", v5: {graph: "live"}, v6: {graph: "run19", alsoServes: ["run15"]} }
```
Factory jawab `isSeedifyToken` / `curveOf`, jadi frontend bisa nemuin run mana yang punya token tertentu.

## Cara pakai di project gw
Buat launchpad/factory sendiri: deploy immutable, versi-in di file config frontend dengan `deployBlock` + `runtimeHash` + feature flags, dan bikin lookup "token ini milik factory mana". Cek runtime hash pas app boot.

## Caveat / jangan ditiru
- Bug di run lama gak bisa di-patch. Yang bisa cuma matiin launch baru (`setLaunchEnabled(false)`) dan pindah ke run baru.
- Config makin gede tiap run. Bundle mereka bawa banyak graph sekaligus.
- Pin hash gak ada gunanya kalau source-nya unverified: lu tahu bytecode-nya gak berubah, tapi gak tahu isinya apa.

## Bukti
- `domain-shared-YxvjzOAA.js` (snapshot recon) (`v5Graphs`, `v6Graphs`), `gate-core-*.js` (env + `seal`)
- `GET /api/v1/chains/46630/config` → `legacyPublicGraphs[].runtimeHashes`, `deploymentVersion: testnet-r3.10.6b905a4c`
- Semua address run19: slot EIP-1967 kosong (bukan proxy)
