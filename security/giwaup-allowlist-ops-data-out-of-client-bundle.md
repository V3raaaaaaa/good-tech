---
name: Data operasional allowlist jangan ikut ke client bundle (pelajaran dari GIWA UP)
category: security
project: GIWA UP (giwaup.xyz)
chain: offchain
tags: [allowlist, whitelist, nextjs, bundle-leak, google-sheets, pii, lesson, anti-pattern]
score: 6
status: verified
added: 2026-11-24
source: recon 2026-11-24, https://giwaup.xyz/ (client bundle), https://giwaup.xyz/api/whitelist
---
# Data operasional allowlist jangan ikut ke client bundle (pelajaran dari GIWA UP)

## Ringkas
Situs WL-nya punya endpoint status yang bener (`GET /api/whitelist?address=` → `{"status": "FREE_MINT_WL" | "PRIORITY_MINT_WL" | "APPLICATION_RECEIVED" | "PUBLIC_MINT" | null}`), tapi file data yang dipakai server ikut ke-import di komponen client. Akibatnya satu chunk JS publik berisi: ID + URL tiga Google Sheet respons form, nama kolom, 14 submission lengkap (timestamp, link post X, 14 wallet free-mint, 38 wallet priority). Ketiga sheet itu juga "anyone with the link", jadi bisa di-export CSV tanpa login, dan satu di antaranya punya kolom email.

Entry ini pelajaran: polanya bagus di sisi API, bocornya di batas server/client.

## Kenapa bagus
- Bagian yang layak ditiru: lookup per alamat, bukan daftar yang bisa di-download. Validasi regex `^0x[a-fA-F0-9]{40}$` → 400 `INVALID_ADDRESS`, method selain GET → 405, timeout 20 detik di client.
- Status punya ranking (`free-mint 3 > priority-mint 2 > application-received 1 > public-mint 0`), jadi satu wallet yang muncul di beberapa sumber selalu dapet tier tertinggi. Itu cara rapi buat gabungin beberapa form.
- Tier "application received" ngasih feedback ke pelamar tanpa janji apa-apa.

## Cara kerja
- Tiga form (KOL giveaway, KOL post, community task) → tiga sheet → skrip ekspor jadi satu modul `{sources:[...], submissions:[...]}`.
- Modul itu di-import dua kali: di route handler (bener) dan di komponen marquee/homepage (bocor), jadi Turbopack masukin seluruh objeknya ke chunk client.

## Cara pakai di project gw
- Tandain modul data dengan `import "server-only"` supaya build gagal kalau ke-import dari client component.
- Kalau client butuh sebagian (mis. daftar link post buat marquee), bikin modul turunan yang cuma berisi field itu.
- Sheet respons form: restricted, akses lewat service account. Jangan pernah taruh `spreadsheetId` di kode yang ke-ship.
- CI check sederhana: `grep -rE '0x[0-9a-fA-F]{40}|docs.google.com/spreadsheets' .next/static` harus kosong.
- Kasih rate limit di endpoint lookup, kalau enggak daftar bisa di-enumerate balik dari alamat yang aktif di chain.

## Caveat / jangan ditiru
- Jangan tiru bagian bocornya. Daftar WL yang kebaca publik = target phishing/dusting yang udah tersortir, dan kolom email/Telegram di sheet publik itu PII.
- Snapshot di bundle basi (14 submission) dibanding sheet-nya (124 baris KOL per 2026-11-23). Data "resmi" yang beda antara bundle, API dan sheet bikin sengketa alokasi.
- Seleksi manual "up to 24 hours" tanpa commitment (Merkle root / hash daftar) gak bisa diaudit dari luar.

## Bukti
- Salah satu chunk client publik memuat objek `sources` + `submissions` (`freeMintWallets`, `priorityMintWallets`). Path chunk sengaja tidak ditulis di sini selama datanya masih terbuka.
- API live 2026-11-24: alamat acak → `{"status":null}`; alamat dari daftar free → `{"status":"FREE_MINT_WL"}`; tanpa parameter → 400 `{"error":"INVALID_ADDRESS"}`; POST → 405
- Sheet: `export?format=csv` balikin 307 ke file ekspor tanpa auth untuk ketiga ID (124 / 6 / 32 baris). Isi baris tidak disalin ke sini.
- Sourcemap produksi → 403 (ini bener, tiru).
