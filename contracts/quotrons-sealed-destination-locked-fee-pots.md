---
name: Fee hook dipecah di dalam swap ke pot yang tujuannya dikunci (sealed sinks), tanpa fungsi sweep
category: contracts
project: QUOTRONS
chain: Robinhood Chain 4663
tags: [uniswap-v4, hook, fee-split, treasury, custody, keeper]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, source hook verified + eth_call
---

# Fee hook dipecah di dalam swap ke pot yang tujuannya dikunci, tanpa fungsi sweep

## Ringkas
Hook motong fee 3% di sisi WETH di dalam swap (LP fee pool dipaksa 0). Fee langsung dibagi pakai pecahan tetap per 240 ke empat aliran: bagian creator dikirim langsung tiap swap, dan tiga sisanya numpuk di pot (reflections, burn, LP). **Tiap pot cuma bisa ditarik satu "sink" yang address-nya di-seal sekali** (`configureAndSealSinks` → `sinksSealed = true`). Gak ada fungsi sweep sembarang.

## Kenapa bagus
- Owner gak bisa ngalihin fee ke wallet sendiri setelah seal. Yang bisa narik pot reflections cuma kontrak reflections, dan seterusnya.
- Kalau keeper berhenti, fee tetap numpuk aman di pot ("nothing is stealable"), cuma telat dibayar.
- Pecahan dalam per-240 = pembagian presisi tanpa sisa pembulatan aneh: 2% / 0.6375% / 0.2125% / 0.15%.
- Bagian creator diambil di swap, jadi gak ada langkah custody.
- Converter saham punya tujuan immutable (cuma ke reflections), dengan batas min/max per epoch dan interval.

## Cara pakai di project gw
Hook/kontrak fee apa pun: split di dalam tx, pot per tujuan, `pullX` cuma dari sink yang di-seal sekali, dan jangan ada `withdraw(token, to)` buat owner.

## Caveat / jangan ditiru
- Owner masih bisa `setPaused` hook (tanpa timelock), jadi trading bisa distop.
- Sink yang salah di-seal = permanen. Harus dites di fork sebelum seal.

## Bukti
- Hook [0x62E200Cc8e4D95cf622f40Dd70f407C883EcB0cc](https://robinhoodchain.blockscout.com/address/0x62E200Cc8e4D95cf622f40Dd70f407C883EcB0cc?tab=contract): `sinksSealed()`=true, `launchFeesFinalized()`=true, `reflectionPot`/`burnPot`/`lpPot`, `pullReflections/pullBurn/pullLp`
- Subgraph: 456.49 ETH fee → 304.33 reflections / 97.00 LP / 32.33 burn / 22.82 creator
