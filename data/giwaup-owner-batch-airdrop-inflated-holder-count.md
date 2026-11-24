---
name: Deteksi holder count yang digelembungin lewat owner batch airdrop
category: data
project: GIWA UP (giwaup.xyz)
chain: giwa-sepolia
tags: [recon-method, holders, airdrop, vanity-metric, blockscout, calldata, due-diligence]
score: 7
status: verified
added: 2026-11-24
source: recon 2026-11-24, https://sepolia-explorer.giwa.io/address/0xD77EB2b29E732B957655a4Df38f62a3fEFA00AAA
---
# Deteksi holder count yang digelembungin lewat owner batch airdrop

## Ringkas
Explorer nunjukin "39.841 holders, 49.360 supply" buat NFT testnet. Angka itu bukan permintaan: 37.595 token (76%) dikirim deployer sendiri lewat `ownerMintBatch(address[])` ke alamat orang lain, 32.100 di antaranya dalam satu hari. Mint organik cuma ±11,7 ribu. Cara ngeceknya murah dan bisa dipakai di koleksi mana pun.

## Kenapa bagus
- Tiga request API explorer cukup buat misahin "holder karena mint" dari "holder karena dikirimin".
- Gak butuh ABI atau source terverifikasi: panjang array ada di calldata, word kedua setelah selector.
- Hasilnya angka, bukan kesan: persen supply hasil airdrop + tanggalnya.

## Cara kerja
1. Ambil selector dari bytecode (scan `PUSH4 … EQ`), lookup di database signature → ketemu `ownerMint(address,uint256)` / `ownerMintBatch(address[])`.
2. Paging `GET /api/v2/addresses/<deployer>/transactions` (Blockscout).
3. Untuk tiap tx yang `raw_input` diawali selector batch: `n = int(raw_input[74:138], 16)` (panjang array). Jumlahin per kontrak dan per tanggal.
4. Bandingin dengan `totalSupply()` dan `transactions_count` kontrak. Tx user ≈ mint organik; sisanya airdrop.
5. Cek silang: holder teratas. Di sini maksimum 26 token per wallet, cocok dengan cooldown 12 jam × 25 hari, jadi gak ada whale; penggelembungan murni dari lebar airdrop.

## Cara pakai di project gw
- Masukin ke checklist recon sebelum percaya angka "holders" atau "minted" di landing page.
- Kalau gw sendiri airdrop ke daftar alamat, tulis angkanya terpisah ("minted by users" vs "airdropped"), biar gak dibaca sebagai vanity metric.
- Untuk indexer: tandain token yang `from = 0x0` dan `tx.from = owner` sebagai `airdrop`, bukan `mint`.

## Caveat / jangan ditiru
- Jangan tiru airdrop massal ke alamat acak buat naikin holder count. Di testnet gratis, di mainnet itu spam dan gampang ketahuan dengan cara di atas.
- Metode ini cuma nangkep batch dari deployer/owner. Kalau dikirim dari wallet lain atau lewat kontrak perantara, lacak pemanggil fungsi owner-only dari event `Transfer(0x0 → to)`.
- Airdrop testnet bisa aja niatnya baik (ngajak wallet aktif). Yang dinilai: apakah angkanya diklaim sebagai permintaan organik.

## Bukti
- Deployer `0xD77EB2b29E732B957655a4Df38f62a3fEFA00AAA`: 306 tx, 238 di antaranya `0x6e67a3a1` ke kontrak utama
- Jumlah alamat per tanggal (dari calldata): 2026-10-30 1.545 · 10-31 3.700 · 11-09 1.175 · 11-11 32.100
- Per kontrak: `0x5F1276Cd…44eB` 37.595 · `0x1B675dD5…73e7` 620 · `0xFc9aAD89…D46A` 305 (dua terakhir deploy percobaan di hari yang sama)
- Explorer 2026-11-24: `total_supply 49360`, `holders_count 39841`, `transactions_count 12344` — https://sepolia-explorer.giwa.io/token/0x5F1276Cd1De9f7078d67A877d646Ab3C108444eB
