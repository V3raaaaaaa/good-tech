---
name: Token "warna" CMYK yang ikut pindah proporsional tiap transfer (largest-remainder)
category: contracts
project: BALANCE / Exchange (Jack Butcher)
chain: Ethereum mainnet 1
tags: [erc20, provenance, art-token, rounding, transfer-hook]
score: 7
status: verified
added: 2026-11-11
source: verified source Etherscan 0x3620540c994433D7B4a628C46d2ED5F92572eA07 (LineageWithdrawals.sol, InkMath.sol)
---

# Token "warna" CMYK yang ikut pindah proporsional tiap transfer (largest-remainder)

## Ringkas
ERC-20 yang tiap address-nya nyimpen 4 kuantitas (C, M, Y, K) yang totalnya selalu = saldo. Pas transfer, pengirim ngirim potongan campuran warnanya secara proporsional. Hasilnya "asal-usul" token kebawa tanpa NFT per unit.

## Kenapa bagus
- Provenance agregat dengan biaya storage kecil: 4 × uint128 di 2 slot per address.
- Pembagian pakai **largest-remainder** (`mulDiv` + `mulmod`, sisa dibagi ke channel dengan remainder terbesar, tie C→M→Y→K), jadi gak ada unit yang tercipta/hilang karena pembulatan.
- Warna awal di-set dari data sumber (bit plate CMYK dari NFT yang di-"surrender"), jadi visual wallet = sejarah materialnya.

## Cara kerja
```solidity
function _update(address from, address to, uint256 v) internal override {
  super._update(from, to, v);
  uint256[4] memory moving = InkMath.split(v, inkOf(from)); // proporsional
  _ink[from] -= moving; _ink[to] += moving;
  emit InkMoved(from, to, moving);
}
// split: out[c] = mulDiv(v, w[c], sum); rem[c] = mulmod(v, w[c], sum);
// for (left = v - Σout; left > 0; --left) ++out[argmax(rem)], rem[argmax] = 0;
```
Release dari reserve pakai warna yang dihitung saat surrender (`_releaseInk`), bukan warna reserve.

## Cara pakai di project gw
Token art / token yang mau nunjukin "asal" (misal per-season, per-pool, per-faction) tanpa NFT per unit. Visual wallet/token di-render dari 4 angka itu.

## Caveat / jangan ditiru
- Tiap transfer nulis 2×2 slot ink + history → gas transfer jauh lebih mahal dari ERC-20 biasa (108k gas ke address lama).
- Warna nempel ke **address custody**: Uniswap v4 PoolManager nyampur semua pool jadi satu campuran.
- `split` revert `EmptyInk` kalau sum ink 0 tapi saldo > 0. Invariant harus dijaga ketat, kalau gak transfer bisa ke-brick.
- Siapa pun bisa "ngecat" wallet orang dengan transfer kecil yang gak diminta.

## Bukti
- `src/experimental/InkMath.sol`, `LineageWithdrawals.sol::_update` (verified, solc 0.8.28)
- Fork test (snapshot recon): transfer 1,000 BALANCE ke address yang udah punya saldo = 108,110 gas
