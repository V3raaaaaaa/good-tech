---
name: WL signup via X OAuth2 PKCE (scope minimal) + paste address, tanpa wallet connect
category: security
project: Weird Cats
chain: -
tags: [oauth2, pkce, x-login, whitelist, no-signature, anti-drainer]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://weirdcats.xyz/weirdlist/room-v2/ + https://weirdcats.xyz/weirdlist/printer/printer.js
---
# WL signup via X OAuth2 PKCE (scope minimal) + paste address, tanpa wallet connect

## Ringkas
Daftar whitelist cuma butuh login X (OAuth 2.0 Authorization Code + PKCE S256, scope `tweet.read users.read`) lalu user paste address EVM ke input teks. Gak ada wallet connect, gak ada signature, gak ada library web3 di frontend.

## Kenapa bagus
- Nol permukaan drainer: situs gak pernah minta signature, jadi phishing clone yang minta "sign to join WL" langsung keliatan palsu. Pesan "No connect, no signature, never a seed phrase" bisa dipegang.
- Scope X minimal: app gak bisa posting atau DM atas nama user, jadi user lebih mau login.
- Bundle jadi ringan karena gak perlu wagmi/viem/WalletConnect.
- Identitas sybil-nya nempel ke akun X (umur akun, follower) yang bisa difilter server-side.

## Cara kerja
1. Tombol "Insert coin" redirect ke `api.php?a=x_login` (top-level window, biar bisa keluar dari iframe).
2. Server generate `state` + `code_verifier`, simpan di cookie `wl_xauth` (`Secure; HttpOnly; SameSite=Lax`, Max-Age 1 hari), lalu 303 ke `https://x.com/i/oauth2/authorize?...&scope=tweet.read%20users.read&code_challenge_method=S256`.
3. Callback `api.php?a=x2_callback` tukar code ke token, ambil `@handle`, bikin session.
4. Kode referral (`?ref=`) ikut dibawa lewat sign-in dan disimpan server-side, jadi tetap kebaca walau X nyelesain login di browser lain.
5. Frontend validasi address pakai regex `^0x[0-9a-fA-F]{40}$` lalu POST `{cat, wallet}` ke `a=print`.

## Cara pakai di project gw
- Pakai flow ini buat WL/allowlist/raffle yang outputnya cuma daftar address. Kalau nanti butuh bukti kepemilikan address, minta signature SIWE di step terpisah dan jelasin kenapa, jangan dicampur di signup.
- Simpan PKCE verifier di cookie HttpOnly per-attempt, jangan di localStorage.
- Tambah checksum EIP-55 di server biar typo address ketahuan.

## Caveat / jangan ditiru
- Paste address = gak ada bukti user punya address itu. Orang bisa daftarin address siapa aja (termasuk address exchange). Kalau hadiah nyampe ke address itu, aman; kalau dipakai buat "1 wallet 1 entry", gampang di-sybil.
- Scope tanpa `follows.read` artinya syarat "follow akun project" gak bisa dicek pakai token user. Di project ini follower 4.5k tapi tiket 6.3k, jadi follow-gate-nya praktis honor system.
- Kalau mau cek umur akun / follow, butuh X API tier berbayar di server.

## Bukti
- Redirect OAuth (GET `https://weirdcats.xyz/weirdlist/api.php?a=x_login`): 303 ke `x.com/i/oauth2/authorize` dengan `scope=tweet.read users.read`, `code_challenge_method=S256`, cookie `wl_xauth; secure; HttpOnly; SameSite=Lax`.
- `https://weirdcats.xyz/weirdlist/printer/printer.js` baris 16 (`WALLET_RE`), 280-285 (redirect top window + ref), 306 (catatan "read only. we keep your @, never post or DM"), 350-360 (form paste address), 396 (`api('print', {cat, wallet})`).
- `https://weirdcats.xyz/docs/weirdlist.html`: "No connect, no signature, never a seed phrase."
