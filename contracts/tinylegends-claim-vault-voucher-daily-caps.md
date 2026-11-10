---
name: Claim vault voucher EIP-712 + cap harian per wallet & global on-chain
category: contracts
project: Tiny Legends
chain: Robinhood Chain 4663
tags: [p2e, voucher, eip712, claim, rate-limit, hot-key, game-economy]
score: 8
status: verified
added: 2026-11-11
source: recon 2026-11-11, laporan recon internal
---

# Claim vault voucher EIP-712 + cap harian per wallet & global on-chain

## Ringkas
Reward game disimpan di satu vault kontrak. Server gak ngirim token sendiri, cuma nandatangan voucher `(to, amount, claimId, notBefore, deadline)`. User yang submit `claim()` dan bayar gas. Kontrak nolak voucher yang udah dipakai, belum waktunya, kadaluarsa, atau ngelewatin cap harian per wallet / global.

## Kenapa bagus
- **Bocornya hot key server gak = vault habis.** Penyerang yang pegang `SIGNER_ROLE` paling banyak cuma bisa ngambil `globalDailyCap` per hari (di sini 30M dari 364M), dan per wallet 70k. Ada waktu buat `pause()`.
- `claimId` (bytes32) disimpan di `used()`, jadi replay gak bisa.
- `notBefore` = vesting/cooldown ditegakkan kontrak, bukan cuma UI (game pakai buat delay 30 menit setelah withdraw).
- `deadline` = voucher lama gak bisa dipakai setelah ekonomi berubah.
- Server gak perlu pegang gas atau ngirim tx, dan biaya klaim ditanggung user.
- `burnShare` / `burnDailyCap` / `burnedTotal` / `burnedOn(day)`: burn dari vault juga di-cap per hari, dan keliatan per hari.

## Cara kerja
```solidity
function claim(address to, uint256 amount, bytes32 claimId, uint64 notBefore, uint64 deadline, bytes sig) {
  require(!paused && !used[claimId] && block.timestamp >= notBefore && block.timestamp <= deadline);
  require(hasRole(SIGNER_ROLE, ecrecover(_hashTypedDataV4(...), sig)));
  day = block.timestamp / 1 days;
  require(walletClaimed[to][day] + amount <= walletDailyCap && globalClaimed[day] + amount <= globalDailyCap);
  used[claimId] = true; token.transfer(to, amount);
}
```
Client: `claimVoucher(v)` → calldata `0xe8a2e5d8` + args, dikirim dari wallet user.

## Cara pakai di project gw
Buat game/quest/airdrop apapun yang bayar token dari server: pakai pola voucher ini, bukan transfer dari hot wallet. Pisahin role: `DEFAULT_ADMIN` di multisig/timelock, `SIGNER` di server, dan `setCaps` cuma bisa lewat admin (idealnya timelock).

## Caveat / jangan ditiru
- Di Tiny Legends, `DEFAULT_ADMIN` = **satu EOA** yang bisa `setCaps` + `grantRole`. Cap gak ada artinya kalau admin-nya nakal atau ke-hack. Wajib multisig + timelock.
- Cap per wallet gampang diakalin pakai banyak wallet. Butuh gate lain (activation fee, hold rule, sybil check).
- Kontrak unverified: struktur dibaca dari selector dan calldata client.

## Bukti
- Vault `0xDb4eD5219b12794C53D5B1B44551e92874050B08`: `walletDailyCap()=7e22`, `globalDailyCap()=3e25`, `burnDailyCap()=1e25`, `burnedTotal()=4.45e24`, selector `claim(address,uint256,bytes32,uint64,uint64,bytes)`, `used(bytes32)`, `eip712Domain()`
- `SIGNER_ROLE` + `BURNER_ROLE` → `0x27465dd2dae4c16cefb9ede04769b966ee8d3d79` (RoleGranted log)
- 70 payout ke 67 wallet (`lgnd_transfers.json` (snapshot recon))
