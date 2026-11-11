---
name: Wrapper EIP-1193 yang cuma izinin method akun/jaringan, dedupe request, timeout jelas
category: frontend
project: Bars (Jack Butcher / jack.art)
chain: Ethereum mainnet 1
tags: [wallet, eip-1193, ux, timeout, dedupe]
score: 6
status: verified
added: 2026-11-11
source: /exchange/bars/mint.js (snapshot recon) fungsi G2/j2
---

# Wrapper EIP-1193 yang cuma izinin method akun/jaringan, dedupe request, timeout jelas

## Ringkas
Semua panggilan ke `window.ethereum` lewat satu wrapper: method prompt (`eth_requestAccounts`, `wallet_switchEthereumChain`, `wallet_addEthereumChain`) dan read (`eth_accounts`, `eth_chainId`) aja yang boleh. Request identik yang lagi pending di-share (gak buka popup dobel). Prompt timeout 30 s, read 15 s, pesan error spesifik.

## Kenapa bagus
- Popup wallet dobel ilang (masalah klasik klik "Connect" 2x).
- Read on-chain gak lewat RPC wallet. Pakai RPC publik yang di-pin di CSP, jadi data UI gak tergantung wallet.
- Abort/timeout ngasih pesan "request mungkin masih kebuka di wallet, selesaikan atau cancel dulu" yang bener secara teknis.

## Cara kerja
```js
const PROMPT = new Set(['eth_requestAccounts','wallet_switchEthereumChain','wallet_addEthereumChain'])
const READ = new Set(['eth_accounts','eth_chainId'])
cache = WeakMap<provider, Map<JSON([method,params]), Promise>>
request(p, m, params) => withTimeout(PROMPT.has(m) ? dedupe(p,m,params) : p.request(...), PROMPT.has(m)?30e3:15e3)
```

## Cara pakai di project gw
Copy pola ini ke dApp mana pun: wrapper tunggal, allowlist method, dedupe by `[method, params]`, timeout dengan pesan yang bisa ditindaklanjuti.

## Caveat / jangan ditiru
- Tx tetap harus lewat jalur terpisah (sendTransaction). Wrapper ini sengaja gak nge-handle itu.

## Bukti
- `mint.js`: `D2`/`q2` Set, `j2` timeout, `G2` WeakMap dedupe, error "Only account and network connection requests are allowed here."
