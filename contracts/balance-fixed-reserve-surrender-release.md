---
name: Supply fixed di-mint sekali ke reserve, dirilis cuma lewat surrender NFT dengan receipt guard
category: contracts
project: BALANCE / Exchange (Jack Butcher)
chain: Ethereum mainnet 1
tags: [erc20, nft-to-token, fixed-supply, reentrancy, receipt]
score: 8
status: verified
added: 2026-11-11
source: verified source Etherscan 0x3620540c994433D7B4a628C46d2ED5F92572eA07 (LineageWithdrawals.sol)
---

# Supply fixed di-mint sekali ke reserve, dirilis cuma lewat surrender NFT dengan receipt guard

## Ringkas
Seluruh `maxSupply` (= total rating edisi NFT, 4 desimal → 18 desimal) di-mint ke kontrak itu sendiri di constructor. Token cuma keluar kalau pemilik NFT Statement manggil `withdraw(id, expectedAmount)`, yang narik NFT-nya ke kontrak secara permanen dan transfer `rating × 1e14` token.

## Kenapa bagus
- Gak ada owner, gak ada mint path, gak ada upgrade. Supply bisa diaudit dari satu konstanta.
- `expectedAmount` = quote yang di-review user. Kalau score berubah, revert `ScoreChanged`, jadi gak bisa ketipu angka.
- `onERC721Received` cuma nerima transfer yang lagi diinisiasi `withdraw()` sendiri (`_receivingId`/`_receivingFrom`). NFT yang dikirim sembarangan ditolak.
- Recovery path sempit: cuma NFT setoran nyasar yang **belum** pernah rilis token, dan cuma ke wallet konstanta (bukan ENS, bukan parameter).
- Token yang dikirim balik ke reserve terkunci dan **gak** mengembalikan hak konversi (`totalReleased` gak turun).

## Cara kerja
```solidity
constructor(...) { _mint(address(this), maxSupply); }
function withdraw(uint256 id, uint256 expected) external nonReentrant {
  require(statements.ownerOf(id) == msg.sender);
  amount = quote(id); if (amount != expected) revert ScoreChanged(amount);
  receipts[id] = Receipt(msg.sender, amount); totalReleased += amount;
  _receivingId = id; _receivingFrom = msg.sender;
  statements.safeTransferFrom(msg.sender, address(this), id); // guard di onERC721Received
  statements.setFormat(id, withdrawnFormat);                // NFT tampil "WITHDRAWN"
  _transfer(address(this), msg.sender, amount);
}
```

## Cara pakai di project gw
NFT → token "fractional by score" tanpa admin: reserve di constructor, release 1:1 atas score yang immutable, guard receipt, recovery ke alamat konstanta.

## Caveat / jangan ditiru
- Reserve yang belum dirilis (di sini ~36.5M dari 53.75M) = **overhang**: pemegang NFT yang belum convert bisa kapan aja convert lalu jual.
- Dependency ke kontrak Statements + registry renderer-nya (trusted).
- FDV menyesatkan: harga × maxSupply ≠ likuiditas.

## Bukti
- `LineageWithdrawals.sol` (verified), `maxSupply = 537_523_867_072 * 1e14`
- On-chain (snapshot recon): `balanceOf(token itself)` = 36,500,341.88 BALANCE (unreleased), totalSupply 53,750,000
