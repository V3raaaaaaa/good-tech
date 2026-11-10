---
name: Bot self-registration + human claim code
category: backend
project: Tiny Legends (tinylegends.fun)
chain: -
tags: [ai-agents, onboarding, api-keys, skill-md, anti-sybil]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://tiny-legends-production.up.railway.app/skill.md
---
# Bot self-registration + human claim code

## Ringkas
AI agent bisa daftar sendiri lewat satu POST, dapet `api_key` (prefix `tiny_live_`) + `claim_code` 8 karakter. Agent-nya belum bisa ngapa-ngapain sampe manusia pemiliknya "claim" pake claim code + early-access code. Seluruh flow didokumentasiin di satu file `skill.md` yang bisa langsung dibaca LLM agent.

## Kenapa bagus
- Agent bisa onboard tanpa browser, tanpa OAuth, tanpa wallet.
- Tapi kuota/aksi berbiaya (generate karakter pake LLM) tetap nempel ke manusia yang punya invite. Satu invite = satu owner, jadi bot farm gak bisa bikin akun bernilai tanpa invite.
- Status `unclaimed` → `claimed` jelas, error code-nya eksplisit (403 kalo belum di-claim, 409 kalo udah di-claim).
- Rate limit beda per endpoint: register 3/jam/IP, claim 10/menit/IP, create 8/menit, chat 12/menit.

## Cara kerja
1. `POST /api/v1/agents/register {agent_name, type:"bot"}` → `{agent_id, api_key, claim_code, status:"unclaimed"}`.
2. Agent ngasih `claim_code` ke ownernya (lewat chat, dsb).
3. Owner `POST /api/v1/agents/claim {claim_code, access_code}`. Server ngiket agent ke owner yang punya early-access code itu.
4. Semua endpoint lain pake `Authorization: Bearer tiny_live_...`. Key gak bisa di-recover (cuma disimpan hash-nya, kemungkinan besar).
5. `skill.md` disajikan sebagai `text/markdown` dengan frontmatter (`name`, `base_url`, `auth_type`, `auth_prefix`) biar agent framework bisa parse otomatis.

## Cara pakai di project gw
- Buat API yang mau dipake agent: kasih register publik yang murah, tapi semua aksi mahal digate di "claimed".
- Claim pake sesuatu yang langka (invite, akun berbayar, login X), jangan cuma email.
- Prefix key (`xxx_live_`) biar gampang di-detect secret scanner (GitHub push protection dsb).
- Taruh `skill.md` di root dengan contoh curl lengkap plus tabel rate limit.

## Caveat / jangan ditiru
- `base_url` di skill.md mereka nunjuk ke `https://tinylegends.fun`, padahal API di domain itu (Vercel) jalan dengan DB mati (`/api/health` → `{"ok":false,"db":"down"}`). API yang hidup ada di `*.up.railway.app`. Pastiin base_url di dokumen agent beneran hidup, dan pasang monitor buat itu.
- Frontend mereka nyimpen API key di `localStorage` (`tiny-api-key`) tanpa CSP. Buat key yang dipake manusia lewat browser, mending httpOnly cookie, atau minimal pasang CSP ketat.
- Rate limit per-IP gampang di-rotate pake proxy. Yang beneran ngelindungin itu gate claim-nya.

## Bukti
- https://tiny-legends-production.up.railway.app/skill.md (frontmatter, flow, tabel rate limit)
- https://www.tinylegends.fun/api/health → 503 `db:"down"`, vs https://tiny-legends-production.up.railway.app/api/health → `db:"up"`
