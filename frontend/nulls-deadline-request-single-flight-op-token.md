---
name: Request ber-deadline + single-flight op token biar jawaban telat gak ngubah layar
category: frontend
project: NULLS (nulls.world)
chain: -
tags: [abortcontroller, race-conditions, retries, spa, ux]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://nulls.world/ (inline app script, publik)
---
# Request ber-deadline + single-flight op token biar jawaban telat gak ngubah layar

## Ringkas
Tiap request penting dibungkus helper `ask(fn, op)`. Helper ini pasang `AbortController` dengan deadline (sekitar 10 s), retry otomatis sekali kalau gak ada jawaban, dan hasilnya dibuang kalau `op` udah bukan op terbaru. Cuma boleh ada satu check yang jalan. Mulai check baru atau nutup panel akan abort request lama dan membatalkan retry-nya. Tiap navigasi juga naikin `waitId`, jadi callback dari layar lama gak punya efek.

## Kenapa bagus
- Nutup bug "jawaban telat nimpa layar baru" (misalnya user udah balik ke menu, terus response lama tiba-tiba buka card atau redirect ke X).
- Error dibedain dengan jelas: gak ada jawaban (NO SIGNAL), server error/5xx (BUSY), belum dikonfigurasi (`not_ready` → OFFLINE), 429 (LIMIT). User dapat pesan yang jujur, bukan spinner tanpa ujung.
- Worst-case waktu tunggu bisa dihitung dan didokumentasikan (sekitar 21 s: 10 + 0.8 + 10).
- Fire-and-forget yang penting (catatan "share tap") pakai `fetch(..., {keepalive:true})` plus backoff 2/5/15/30/60 s. Payload-nya `ageMs` sejak tap, jadi server bisa nerima event telat dalam jendela 15 menit.

## Cara kerja
```js
ask(make, op) {
  const ctl = new AbortController(), t = setTimeout(() => ctl.abort(), WAIT);
  return make(ctl.signal).then(r => r.json().then(j => ({ r, j })))
    .catch(() => null).finally(() => clearTimeout(t))
    .then(res => (op !== this.currentOp ? null : res)); // op basi → dibuang
}
// caller: null → retry sekali (op yang sama) → masih null → NO SIGNAL
```

## Cara pakai di project gw
- Pakai di mint/claim UI: tombol claim, polling status tx, cek WL. Semua yang bisa telat dan bikin redirect atau ngubah layar.
- Simpan `opId` di instance komponen dan naikin tiap user navigasi. Semua `setState` setelah await harus cek `opId` dulu.

## Caveat / jangan ditiru
- Retry cuma aman kalau endpoint-nya idempotent di server. Abort di client gak membatalkan efek yang udah terjadi di server.
- Komentar kode di sumbernya super panjang dan berbau tulisan agent. Polanya bagus, gaya komentarnya gak usah ditiru.

## Bukti
- Script inline https://nulls.world/ : "One request with a deadline: { r, j } once an answer arrived, or null ... A request that gets no answer in time is aborted"; "One code check at a time ... its request is aborted, its automatic retry never goes out, and nothing it learns is kept"; share tap dikirim dengan `keepalive: true` + body `{ ageMs: Date.now() - tapAt }`.
