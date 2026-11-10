---
name: Karakter brand dijadiin pet di Codex/ChatGPT desktop sebagai distribusi gratis sebelum launch
category: frontend
project: Weird Cats
chain: -
tags: [distribution, codex-plugin, chatgpt, mascot, pre-launch, growth]
score: 5
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://github.com/nett0eth/weird-cats-codex-pets + https://weirdcats.xyz/docs/codex-pets.html
---
# Karakter brand dijadiin pet di Codex/ChatGPT desktop sebagai distribusi gratis

## Ringkas
Sebelum ada NFT, 25 karakter project dirilis gratis sebagai "Codex Pet" (pet animasi yang nunjukin status agent: working / waiting / done) lewat marketplace plugin Codex, plus versi felt buat ChatGPT desktop. User install pakai dua command, lalu karakternya nongol di layar tiap hari.

## Kenapa bagus
- Karakter lu nongol di layar developer berjam-jam per hari. Exposure kayak gini gak bisa dibeli lewat iklan.
- Gak butuh wallet, jadi audience-nya keluar dari bubble crypto.
- Install-nya jadi konten share sendiri ("cat gw nemenin Codex").
- Distribusi lewat GitHub repo = gratis, versioned, bisa di-fork.

## Cara kerja
- Repo jadi Codex plugin marketplace: `codex plugin marketplace add <owner>/<repo>` lalu `codex plugin add weird-cats@weird-cats`.
- Plugin bawa sebuah skill (`SKILL.md`) yang ngajarin agent: kalau user ketik `$weird-cats <nama>`, jalanin `scripts/install_pet.py <nama>`.
- Script copy `pet.json` + `spritesheet.webp` (sprite v2, 16 arah ikut cursor) ke `~/.codex/pets/<id>`, user tinggal Settings, Pets, Refresh.
- Varian felt ("Plush Pets") pakai installer shell/PowerShell + deeplink.

## Cara pakai di project gw
- Kalau project punya karakter/mascot: bikin pack pet/skin buat tool yang dipakai audience tiap hari (Codex, terminal theme, VS Code, Discord sticker, GIPHY).
- Format paket: zip dengan manifest + sprite, installer yang validasi isinya (lihat entry installer strict-zip).
- Kasih CTA halus ke situs di README, bukan di pet-nya.

## Caveat / jangan ditiru
- Format pet milik pihak ketiga (OpenAI) dan bisa berubah kapan aja; project ini sendiri ngaku script macOS belum dites di Mac beneran.
- Trademark: wajib disclaimer "not affiliated" (project ini pasang di docs).
- Jangan distribusi lewat `curl | sh` dari branch yang gak di-pin.
- Traction GitHub-nya kecil (1 star per repo), jadi efek distribusinya belum terbukti dari data publik. Yang verified cuma tekniknya.

## Bukti
- https://github.com/nett0eth/weird-cats-codex-pets (`plugins/weird-cats/skills/weird-cats/SKILL.md`, `plugins/weird-cats/scripts/install_pet.py`, `plugins/weird-cats/assets/pets/*.zip`)
- https://github.com/nett0eth/weird-cats-plush-pets (`install/install.sh`, `install/install.ps1`, `install/make-deeplinks.mjs`)
- https://weirdcats.xyz/docs/codex-pets.html, https://weirdcats.xyz/docs/faq.html
