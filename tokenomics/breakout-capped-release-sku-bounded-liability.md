---
name: SKU rilis terbatas buat produk yang sengaja "kemurahan" (liabilitas dibatesin jumlah unit)
category: tokenomics
project: Breakout (breakoutprop.com)
chain: offchain
tags: [pricing, limited-release, loss-leader, risk-cap, prop-firm, launch]
score: 7
status: verified
added: 2026-11-24
source: recon 2026-11-24, https://www.breakoutprop.com/products/spark/ , https://intercom.help/breakoutprop/en/articles/17230339-how-many-spark002-evaluations-are-available-at-launch , https://intercom.help/breakoutprop/en/articles/18514860-what-is-the-difference-between-spark001-and-spark002
---
# SKU rilis terbatas buat produk yang sengaja "kemurahan"

## Ringkas
Produk dengan aturan paling longgar (Spark: akun $50K, target $3.000, trailing loss $1.500, tanpa daily loss / consistency / min hari) dijual murah ($139, lalu $99) tapi cuma 1.500 unit per rilis, bernomor (001, 002). Tiap rilis aturannya dikoreksi dari data rilis sebelumnya.

## Kenapa bagus
- Produk yang secara matematis paling menguntungkan pembeli tetap bisa dijual, karena kerugian maksimum operator = unit × nilai opsi per unit. Angkanya ketahuan dari awal.
- Nomor rilis bikin perubahan aturan jadi produk baru, bukan "aturan diubah di tengah jalan". Pemegang 001 tetap pakai aturan 001.
- "Sold out" + waitlist jadi mesin marketing gratis.
- Tiap rilis = eksperimen terkontrol. 001 → 002 mengubah satu variabel (high-water mark ikut profit terbuka) dan harga turun ~30%.

## Cara kerja
- Counter stok di server, checkout nolak setelah N.
- Aturan di-versi per SKU dan nempel ke akun seumur hidup akun itu.
- Halaman bantuan punya artikel "apa bedanya 001 vs 002" dan "apakah aturan 002 berlaku ke akun 001" (jawabannya: nggak).

## Cara pakai di project gw
- Mint / pass / tier dengan parameter agresif: rilis bernomor dengan cap unit, jangan open-ended.
- Hitung dulu worst case = unit × payout maksimum yang masuk akal. Kalau angka itu gak sanggup ditanggung, kecilin cap, jangan ubah aturan belakangan.
- Simpan versi aturan di record tiap item, bukan di config global.

## Caveat / jangan ditiru
- Cap unit gak nolong kalau satu orang bisa beli banyak. Breakout tetap butuh KYC + larangan multi-akun per rumah/device/IP buat itu.
- Aturan 002 punya jebakan yang gampang salah paham (floor naik sekali sehari pakai high yang sudah lewat). Kalau aturannya butuh artikel "kenapa akun gw breach padahal profit", itu tanda desainnya terlalu licin.

## Bukti
- Halaman produk: "All 1,500 evaluations in this release have sold."
- Help center: Spark002 "limited to 1,500 accounts", "prices are ~30% lower than Spark001".
