---
name: Env schema bertipe dengan release stage + signer mode (KMS/key) + health endpoint
category: infra
project: Yield Fields
chain: -
tags: [nextjs, t3-env, zod, feature-flags, aws-kms, health-check]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, bundle publik https://yieldfields.fun/_next/static/immutable/chunks/1t-sqjs9f-o7u.js, https://yieldfields.fun/api/health
---
# Env schema bertipe dengan release stage + signer mode (KMS/key) + health endpoint

## Ringkas
Semua konfigurasi server divalidasi pakai `createEnv` (t3-env) + zod: tipe URL, regex private key 32-byte, regex IAM role ARN, enum flag `on|off`. Ada satu knob `YF_PUBLIC_RELEASE` (`off|pre|mint|play`) yang nentuin env mana yang **wajib**. Tiap signer punya dua mode (KMS key id atau raw key), dan `/api/health` ngelaporin signer address + mode + status db/redis/rpc.

## Kenapa bagus
- Deploy salah config gagal di boot, bukan pas user lagi mint.
- Release staging (pre → mint → play) + flag per fitur (`YF_FLAG_PLAY_SHOP`, `..._DEEDS_BURNS`, dll) bikin fitur bisa dibuka bertahap tanpa redeploy kode.
- Cross-field rules: mis. `YF_FERT_RATE_CLOCK=chain` cuma boleh di deployment lokal; release ≠ off wajib punya `DATABASE_URL` + RPC publik.
- Health endpoint publik yang nggak bocorin rahasia tapi cukup buat monitoring (signer berubah = alert).

## Cara kerja
- `server: { DATABASE_URL: z.string().refine(postgres://…), IRON_SESSION_PASSWORD: z.string().min(32), YF_*_SIGNER_PRIVATE_KEY: z.string().regex(/^0x[0-9a-fA-F]{64}$/), AWS_ROLE_ARN: z.string().regex(/^arn:aws[\w-]*:iam::\d{12}:role\/.+$/), YF_PUBLIC_RELEASE: z.enum([...]).default("off"), ... }` + `superRefine` buat aturan antar field.
- `/api/health` → `{"signers":{"minter":"0x91c0…"},"signerModes":{"minter":"kms"},"checks":{"db":"ok","redis":"ok","rpc":"ok"}}`.

## Cara pakai di project gw
- Pakai `@t3-oss/env-nextjs`, satu file `env.ts`, import cuma dari kode server.
- Tambahin enum release stage + `superRefine` buat env wajib per stage.
- Signer factory: kalau `*_KMS_KEY_ID` ada → KMS account, else raw key (dev only). Health endpoint ngelaporin mode-nya.

## Caveat / jangan ditiru
- Di sini schema server (nama semua env, termasuk `TURNSTILE_SECRET_KEY`, `CRON_SECRET`, KMS key var) **ikut ke-bundle ke client**. Nilainya nggak bocor (masih `process.env`), tapi peta backend jadi kebaca. Pisahin modul env server pakai `import "server-only"`.
- Health endpoint publik sebaiknya tetap minimal; jangan expose versi dependency atau error detail.

## Bukti
- Schema `createEnv({server:{DATABASE_URL…,YF_PUBLIC_RELEASE…,YF_MINTER_SIGNER_KMS_KEY_ID…}})` di https://yieldfields.fun/_next/static/immutable/chunks/1t-sqjs9f-o7u.js.
- https://yieldfields.fun/api/health (GET publik).
