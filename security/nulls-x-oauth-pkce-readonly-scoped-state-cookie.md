---
name: X OAuth 2.0 PKCE read-only + state cookie yang di-scope ke path auth
category: security
project: NULLS (nulls.world)
chain: -
tags: [oauth, pkce, x-login, cookies, least-privilege]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://nulls.world/api/auth/x/start (redirect header publik)
---
# X OAuth 2.0 PKCE read-only + state cookie yang di-scope ke path auth

## Ringkas
Login X pakai OAuth 2.0 Authorization Code + PKCE (S256), scope cuma `tweet.read users.read`. State/verifier PKCE disimpan di cookie terpisah yang HttpOnly, Secure, SameSite=Lax, `Path=/api/auth/x`, umur 900 detik, lalu dihapus (Max-Age=0) begitu callback jalan, berhasil atau gagal.

## Kenapa bagus
- Least privilege: app WL/quest cuma butuh tahu siapa user dan apakah dia nge-post. Tanpa `tweet.write`/`follows.write`/`offline.access`, token yang bocor gak bisa dipakai buat posting atas nama user.
- Cookie state cuma dikirim browser ke route `/api/auth/x/*`, jadi gak ikut nempel di request API lain dan gak bisa dibaca JS.
- TTL 15 menit + dihapus di callback, jadi state gak bisa di-replay.
- Callback yang dipanggil tanpa state langsung redirect `/?x=error` dan menghapus cookie: gagalnya bersih, gak 500.

## Cara kerja
1. `GET /api/auth/x/start?for=<flow>` → bikin `state` + `code_verifier`, simpan (signed) di cookie `xauth` dengan `Path=/api/auth/x; Max-Age=900`, redirect 302 ke `x.com/i/oauth2/authorize?...&code_challenge_method=S256`.
2. X redirect balik ke `/api/auth/x/callback?code&state`.
3. Callback mencocokkan state dengan cookie, tukar code + verifier jadi token, ambil profil, bind ke session, set `Max-Age=0` di cookie xauth, lalu redirect `/?x=<result>&for=<flow>`.
4. Frontend baca `?x=` sekali saja, lalu `history.replaceState` biar hasilnya hilang dari URL.

## Cara pakai di project gw
- Template: satu route start + satu callback serverless. Param `for=` dipakai buat routing hasil ke layar yang benar (apply/list/connect) tanpa nyimpan state tambahan.
- Hasil callback dibatasi ke enum kecil (`applied|denied|error|busy|...`) biar URL gak bisa disuntik pesan bebas.
- Butuh verifikasi share? Cukup `tweet.read` plus cek server-side, gak perlu scope write.

## Caveat / jangan ditiru
- Scope read-only artinya task follow/like/repost gak bisa diverifikasi. Kalau butuh bukti follow, lu harus pakai endpoint X berbayar.
- Cookie state harus di-sign/encrypt (HMAC). Jangan simpan verifier mentah tanpa integritas.
- `SameSite=Lax` cukup buat redirect top-level dari X. Jangan pakai `Strict`, karena cookie gak bakal ikut di redirect cross-site.

## Bukti
- Varian lain di RebelKin (https://rebelkin.xyz): sama-sama PKCE S256 + scope `tweet.read users.read`, **tanpa `offline.access`** (gak ada refresh token yang bisa bocor), state cookie `rk_oauth` 10 menit, dan semua request yang ngubah state wajib bawa header `X-CSRF-Token` yang dikasih server lewat `GET /api/me`.
- Versi "WL tanpa wallet connect" dari pola ini: lihat entry `security/weirdcats-x-oauth-pkce-paste-address-wl.md`.
- `curl -sI "https://nulls.world/api/auth/x/start?for=connect"` → `location: https://x.com/i/oauth2/authorize?response_type=code&...&scope=tweet.read+users.read&...&code_challenge_method=S256` dan `set-cookie: nulls_xauth=...; Path=/api/auth/x; Max-Age=900; HttpOnly; Secure; SameSite=Lax`.
- `curl -sI https://nulls.world/api/auth/x/callback` → `302 location: /?x=error` + `nulls_xauth=; Max-Age=0`.
