---
name: NFT reveal pakai block delay + offset, dan perk berdasarkan lama hold (heldSince)
category: contracts
project: Tiny Legends (Founders NFT)
chain: Robinhood Chain 4663
tags: [nft, reveal, randomness, holding-perk, erc721]
score: 6
status: claimed
added: 2026-11-11
source: recon 2026-11-11, selector Founders 0x5568f87DcB71222651A10c06Db83df4834D75164
---

# NFT reveal pakai block delay + offset, dan perk berdasarkan lama hold (heldSince)

## Ringkas
Koleksi Founders (1111) di-reveal dua langkah: admin manggil `reveal()` yang nyatet `revealBlock`, terus setelah `REVEAL_DELAY` (5 block) siapa pun bisa `lockReveal()` yang ngambil `offset` dari blockhash block itu. Tier tiap NFT = `(id + offset) % N`. Ditambah `heldSince(tokenId)`: perk in-game (cap +%) baru aktif setelah NFT dipegang 24 jam di wallet yang sama.

## Kenapa bagus
- Offset dari blockhash *setelah* reveal dipanggil, jadi admin gak bisa milih hasil di tx yang sama, dan minter gak tahu tier pas mint.
- Lebih murah dan simpel dari VRF buat chain yang gak punya Chainlink VRF (kayak Robinhood Chain).
- `heldSince` direset tiap transfer, jadi NFT gak bisa "disewa" sebentar buat dapet perk (anti flash-borrow / anti sharing).
- `tierOf(id)` on-chain = game baca tier langsung dari kontrak, gak bisa dibohongin metadata.
- `TEAM_RESERVE` (61) dan `teamMinted` keliatan on-chain, `maxPerWallet` 3, royalty 5% (ERC-2981).

## Cara kerja
```
reveal()      -> revealBlock = block.number            (admin)
lockReveal()  -> require(block.number > revealBlock + REVEAL_DELAY); offset = uint(blockhash(revealBlock + REVEAL_DELAY)) % MAX_SUPPLY
tierOf(id)    -> tierTable[(id + offset) % MAX_SUPPLY]
_update(from,to,id) -> heldSince[id] = block.timestamp
game: perk aktif kalau now - heldSince[id] >= 24h && ownerOf(id) == player
```

## Cara pakai di project gw
Buat NFT launch di chain tanpa VRF: commit block + delay + blockhash offset. Buat perk holder: simpan `heldSince` per token di `_update`, dan backend cek umur hold, bukan cuma `balanceOf`.

## Caveat / jangan ditiru
- Blockhash bisa dipengaruhi sequencer (L2 dengan satu sequencer kayak Robinhood Chain). Itu satu pihak yang secara teori bisa milih. Jangan pakai buat hadiah bernilai besar.
- `blockhash` cuma tersedia 256 block terakhir. Kalau `lockReveal` telat, harus ada fallback.
- **Status `claimed`:** koleksi belum di-mint (phase 0) dan kontrak unverified. Mekanisme di atas disimpulkan dari nama selector (`revealBlock`, `REVEAL_DELAY`, `offset`, `lockReveal`, `heldSince`, `tierOf`) + string UI ("A Founder counts after 24 h in your wallet"), belum dilihat jalan.

## Bukti
- Founders `0x5568f87DcB71222651A10c06Db83df4834D75164`: `MAX_SUPPLY()=1111`, `maxPerWallet()=3`, `TEAM_RESERVE()=61`, `REVEAL_DELAY()=5`, `royaltyBps()=500`, `phase()=0`
