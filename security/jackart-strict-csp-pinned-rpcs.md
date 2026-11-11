---
name: CSP ketat yang nge-pin RPC yang boleh dipanggil dApp
category: security
project: Exchange / Bars (jack.art)
chain: Ethereum mainnet 1
tags: [csp, headers, rpc, supply-chain]
score: 6
status: verified
added: 2026-11-11
source: response header https://jack.art/exchange/bars
---

# CSP ketat yang nge-pin RPC yang boleh dipanggil dApp

## Ringkas
Static dApp tanpa script pihak ketiga: `script-src 'self'`, `connect-src` cuma ke 4 RPC Ethereum, `frame-ancestors 'none'`, `base-uri 'none'`, `form-action 'self'`. Plus `referrer-policy: no-referrer` dan `permissions-policy` yang matiin kamera/mic/geo.

## Kenapa bagus
- Kalau ada XSS/inject, script gak bisa exfil ke domain lain atau load lib dari CDN.
- Anti-clickjacking (gak bisa di-iframe) penting buat halaman yang minta approve/sign.
- RPC fallback (Tenderly, publicnode, dRPC, MEV Blocker) eksplisit, sekaligus jadi dokumentasi.

## Cara kerja
```
content-security-policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
  img-src 'self' https://jack.art data:; connect-src 'self' https://mainnet.gateway.tenderly.co
  https://ethereum-rpc.publicnode.com https://eth.drpc.org https://rpc.mevblocker.io;
  object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'
```

## Cara pakai di project gw
Bundle semua dependency (viem dll) ke file sendiri, lalu pasang CSP ini dan ganti `connect-src` ke RPC/API sendiri.

## Caveat / jangan ditiru
- `?rpc=` override di query string tetap kepentok CSP, jadi user gak bisa pakai RPC custom di situs resmi.
- `style-src 'unsafe-inline'` masih kebuka.

## Bukti
- `curl -D- https://jack.art/exchange/bars` (2026-11-11)
