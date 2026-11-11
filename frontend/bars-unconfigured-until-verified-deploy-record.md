---
name: Frontend mode "unconfigured" sampai deploy record terverifikasi (hash, waktu, root di-cross-check)
category: frontend
project: Bars (Jack Butcher / jack.art)
chain: Ethereum mainnet 1
tags: [deployment, integrity, runtime-hash, config, phishing-defense]
score: 8
status: verified
added: 2026-11-11
source: /exchange/bars/mint.js (snapshot recon)
---

# Frontend mode "unconfigured" sampai deploy record terverifikasi (hash, waktu, root di-cross-check)

## Ringkas
Bundle punya record `{chainId, token, edition, runtimeHash, deployBlock, mintStart, publicStart, mintEnd, listRoot, listBlock}` yang diisi script deploy/verify **setelah** mainnet deploy. Selama ada field null, UI tampil "Preview, contract not deployed yet" dan tombol mint mati. Setelah diisi, tiap load ngecek semua angka ke chain.

## Kenapa bagus
- Gak ada "address kontrak" yang bisa dibocorin atau di-spoof sebelum waktunya. Link phishing gak bisa nunggang UI resmi.
- Cross-check pas boot: chainId = 1, `balance()` = token yang di-pin, `keccak(getCode)` = `runtimeHash`, `mintStart/mintEnd/publicStart/listRoot` = record. Kalau ada yang beda, UI error dan gak bikin tx.
- 3 mode: `production`, `rehearsal` (localhost + `?edition=` buat anvil, chain 31337), `unconfigured`.
- Helper kedua (buyer `buyAndMint`) punya record sendiri dengan `runtimeHash`.

## Cara kerja
```js
mode = isLocal && q.has('edition') ? 'rehearsal'
     : rec.chainId===1 && isAddr(rec.edition) && isHash(rec.runtimeHash) && rec.deployBlock!=null
       && rec.mintStart!=null && rec.listRoot ? 'production' : 'unconfigured'
assert(keccak256(await getCode(edition)) === rec.runtimeHash)
```

## Cara pakai di project gw
Buat launch sendiri: commit record kosong dulu, deploy, script verify isi record + runtimeHash, baru publish bundle. UI selalu cross-check sebelum nulis tx.

## Caveat / jangan ditiru
- Bot gak bisa siap-siap pakai address dari bundle. Harus watch deployer/bundle pas H-0, jadi ini juga semacam anti-bot ringan.
- Pin hash cuma bilang "bytecode ini yang dimaksud", bukan "bytecode ini aman". Tetap butuh source verified.

## Bukti
- `mint.js`: string "the record deploy/verify-buyer-deploy.mjs writes after the mainnet deployment", record dengan `edition:null`, fungsi mode `production|rehearsal|unconfigured`, error "The contract at the configured address is not the verified Bars deployment."
