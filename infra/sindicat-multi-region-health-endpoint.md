---
name: Server game multi-region dengan /health yang ngelaporin commit, region, DB, dan status config auth
category: infra
project: SINDICAT
chain: -
tags: [multi-region, health-check, observability, railway, deployment]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, `*health.json` (snapshot recon)
---

# Server game multi-region dengan /health yang ngelaporin commit, region, DB, dan status config auth

## Ringkas
Tiga server identik (EU, US, Asia-Pacific) di Railway, dan pemain pilih region. Tiap server punya `/health` yang ngasih tau: commit + branch yang lagi jalan, region, jenis DB, uptime, flag fitur (`act`), versi Node, dan apakah config auth pihak ketiga (Privy app, JWKS, secret) **ada dan valid**, tanpa nampilin secret-nya.

## Kenapa bagus
- Sekali curl ke 3 region langsung keliatan apakah semua udah di commit yang sama (`e11913a`), jadi gak ada region ketinggalan deploy.
- Cek "config lengkap" (`privy: {configured, app:"ok", jwks:"ok", secret:"ok"}`) nangkep env var yang lupa diset sebelum pemain kena error login.
- Uptime + `startedAt` = langsung tahu kalau server crash-loop.
- Murah: Railway per region + satu codebase.

## Cara kerja
```json
GET /health -> {"ok":true,"db":"pg","uptimeS":29331,"startedAt":"2026-11-10T12:04:47Z","commit":"e11913a","branch":"main",
                "region":"EU","act":true,"node":"v24.22.1",
                "privy":{"configured":true,"appId":"cmub…","app":"ok","jwks":"ok","secret":"ok"},
                "accounts":189,"states":77}
```

## Cara pakai di project gw
Tiap service (mint bot, radar, game server): `/health` dengan commit, region, cek koneksi DB, dan cek tiap dependency (RPC, auth, webhook) sebagai `"ok"/"missing"`. Pantau semua region dari satu script atau watcher.

## Caveat / jangan ditiru
- SINDICAT nampilin **jumlah akun dan save** di `/health` publik, info bisnis gratis buat orang luar (termasuk gw). Pisahin `/health` publik (ok/commit) dari `/health/full` yang pakai auth.
- `appId` Privy memang publik, tapi gak perlu diulang di endpoint health.

## Bukti
- `https://sindicat-server-production.up.railway.app/health` (+ `-us-`, `-asia-`): commit sama `e11913a`, region EU/US/ASIA
