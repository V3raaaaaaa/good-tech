---
name: Skill + API buat AI agent: llms.txt, skill.md untuk CLI wallet, endpoint yang ngebangun tx siap preview
category: backend
project: $JAGENT (jager.live)
chain: BNB Smart Chain 56
tags: [ai-agent, llms-txt, skill, tx-builder, eip712-login, wallet-cli]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, jager.live/llms.txt + /skill.md
---

# Skill + API buat AI agent

## Ringkas
Project nyediain tiga lapis buat agent AI: (1) `/llms.txt`: ringkasan kontrak, alamat yang **jangan** dipakai (kontrak lama), dan status live; (2) `/skill.md`: skill lengkap buat CLI wallet (`baw`), dari sign-in, mint, klaim reward, task sosial, binding X, sampai main Boss game; (3) API `/api/agent/mint-tx?address&shares&pay&ref` yang balikin langkah-langkah tx (approve + mint) lengkap dengan command `preview` siap pakai, plus `/api/agent/status` dan `/api/agent/proof` (pesan EIP-712 buat login).

## Kenapa bagus
- Agent gak perlu nebak ABI atau alamat. Server ngebangun calldata, agent cuma preview → tunjukin user → execute.
- Skill nulis **aturan keamanan** eksplisit: tiap tx/tanda tangan wajib preview → konfirmasi user → execute, dan stop kalau preview nampilin risiko.
- Alamat kontrak lama ditulis jelas sebagai "jangan kirim dana", jadi agent gak kirim ke kontrak usang.
- Login pakai bukti EIP-712 berumur 10 menit, gak mindahin dana atau ngasih approval.
- `/api/stats` ngasih kutipan BNB per jumlah share (quote + nilai kirim dengan buffer).

## Cara pakai di project gw
Buat mint/game yang mau dipakai lewat agent (Claude, CLI wallet): sediain `llms.txt`, `skill.md`, dan endpoint "build tx" yang balikin langkah + command preview. Masukin aturan keamanan di skill.

## Caveat / jangan ditiru
- Endpoint build-tx = trust ke server. Agent harus selalu preview/simulasi dan cek tujuan + jumlah.
- Bikin farming multi-akun jadi gampang banget (skill yang sama jalan buat ratusan ID).

## Bukti
- https://jager.live/llms.txt, https://jager.live/skill.md, `GET /api/agent/status?address=`, `GET /api/agent/mint-tx?...`
