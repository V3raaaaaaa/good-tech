---
name: OAuth server MCP sendiri (PKCE, dynamic client) + link login terikat browser asal
category: security
project: mcp.credit (MCP Market)
chain: -
tags: [mcp, oauth2, pkce, phishing, session, x-login]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, /.well-known/oauth-authorization-server + source
---

# OAuth server MCP sendiri (PKCE, dynamic client) + link login terikat browser asal

## Ringkas
Connector MCP pakai OAuth 2.1 standar: `/.well-known/oauth-authorization-server`, dynamic client registration (`/register`), `/authorize` dengan PKCE S256, `/token` (code + refresh), `/revoke`, scope tunggal `market`. Login-nya delegasi ke X (`users.read tweet.read` doang). `/authorize` nge-set cookie `mcp_login_<req>` (Path=/login, 15 menit) di browser yang mulai login, jadi link `/login?req=…` yang di-copy ke browser lain ditolak (403).

## Kenapa bagus
- Jalan langsung di Claude/ChatGPT custom connector tanpa setup manual (dynamic client).
- Link login gak bisa dipakai buat phishing atau "login-in-behalf" (dikirim ke korban terus korban yang login).
- Scope X minimal: gak bisa posting, baca DM, atau follow.
- Token dan code disimpan sebagai hash sha256 di DB.
- Gate umur akun X (≥30 hari) di callback buat ngerem akun bot baru.

## Cara pakai di project gw
Kalau bikin connector MCP sendiri: ikutin spec OAuth MCP (metadata + dynamic registration + PKCE), simpan token sebagai hash, ikat langkah login ke browser asal, dan minta scope sosial seminimal mungkin.

## Caveat / jangan ditiru
- Gate umur akun X cuma rem. Akun X lama bisa dibeli.
- Cookie pengikat cuma 15 menit, jadi user yang lambat harus ulang dari awal.

## Bukti
- `GET https://mcp.credit/.well-known/oauth-authorization-server`
- [server/src/auth.js](https://github.com/davidsyahshi/mcp-market/blob/1bb66c9/server/src/auth.js) (`mcp_login_${id}`)
