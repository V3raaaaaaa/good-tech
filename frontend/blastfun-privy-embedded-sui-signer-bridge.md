---
name: Bridge Privy embedded wallet ke Signer Sui (signRawHash → signPersonalMessage)
category: frontend
project: Blast (blast.fun)
chain: sui
tags: [privy, embedded-wallet, sui, signer, personal-message, onboarding]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, public JS bundle https://www.blast.fun/ (Next.js chunks)
---
# Bridge Privy embedded wallet ke Signer Sui (signRawHash → signPersonalMessage)

## Ringkas
Privy cuma ngasih `signRawHash` buat wallet Sui embedded. Blast bikin subclass `Signer` dari `@mysten/sui` yang `sign(bytes)`-nya diteruskan ke Privy (`hash: 0x<hex>`). Hasilnya semua helper Mysten (`signPersonalMessage`, intent prefix, serialisasi signature) bisa dipake apa adanya.

## Kenapa bagus
- Onboarding 1 klik: login X → wallet Sui langsung jadi → challenge server ditandatangani, tanpa extension.
- Nggak perlu ngerakit intent/serialisasi signature Sui sendiri. Cukup override `sign`, `getKeyScheme`, `getPublicKey`.
- Ada pengaman: public key dari Privy di-parse (hex/base64, 32 byte ed25519 atau berflag), lalu `toSuiAddress()` harus sama dengan address wallet. Kalau beda langsung throw. Signature juga dicek harus persis 64 byte hex.
- Wallet dipilih ketat: `chainType sui`, `connectorType embedded`, `walletClientType privy`, `imported false`, `recoveryMethod privy-v2`.

## Cara kerja
- `class PrivySuiSigner extends Signer { constructor(wallet, signRawHash) { pk = parse(wallet.publicKey); assert(pk.toSuiAddress() === normalize(wallet.address)) } async sign(bytes) { const {signature} = await signRawHash({address, chainType:'sui', hash:'0x'+hex(bytes)}); assert(/^[0-9a-f]{128}$/i); return fromHex(sig) } getKeyScheme(){ return 'ED25519' } }`
- Pemakaian: `new PrivySuiSigner(w, signRawHash).signPersonalMessage(new TextEncoder().encode(challenge))` → `{address, signature}` dikirim ke `/wallet-proof`.
- Flow server: `wallet-challenge` (challengeId, message, expiresAt), lalu `wallet-proof` (verify), lalu `completion` dengan header `Idempotency-Key`.

## Cara pakai di project gw
- App Sui mana pun yang pakai Privy/Dynamic/Turnkey yang cuma ngasih raw-sign: pola ini juga bisa dipake buat `signTransaction` (Signer Mysten yang nge-hash intent message, lu cuma nandatangani digest-nya).
- Gabungin dengan challenge server ber-expiry + idempotency key biar double-submit aman.

## Caveat / jangan ditiru
- Kode frontend blast.fun itu proprietary (bundle publik, bukan repo open source; kontraknya BUSL-1.1). Yang ditiru polanya, bukan kodenya.
- Pastiin yang lu kirim ke `signRawHash` itu bytes yang Mysten serahin ke `sign()` (digest blake2b dari intent message). Jangan nandatangani string mentah.
- Raw-hash signing itu blind signing. Wallet embedded nggak bisa nampilin isi tx, jadi UI app lu yang harus jujur.
- Ini dibaca dari bundle minified, bukan source resmi.

## Bukti
- Bundle publik `https://www.blast.fun/_next/static/immutable/chunks/00gc-ckp3omkc.js` (module 290482: class Signer + check `toSuiAddress() !== address` → "The embedded Sui wallet key does not match its address.")
- Bundle `3gqb3dw7d-dar.js` (module 717805: `createWallet({chainType:"sui"})`, `signEmbeddedMessage`, `signSlushMessage`)
- CSP: `connect-src … https://fullnode.mainnet.sui.io:443 … https://*.rpc.privy.systems` (response header https://www.blast.fun/)
