---
name: Dialog companion yang nempel ke event asli + filter kata duit
category: frontend
project: Tiny Legends (tinylegends.fun)
chain: -
tags: [ai-companion, ethics, retention, deterministic-dialog, anti-dark-pattern]
score: 7
status: verified
added: 2026-11-11
source: recon 2026-11-11, public JS bundle of https://tiny-legends-production.up.railway.app/
---
# Dialog companion yang nempel ke event asli + filter kata duit

## Ringkas
Sapaan harian companion sebagian besar gak dari LLM. Isinya kalimat template per personality (brash/cool/sly/goofy/grumpy/earnest) ditambah "callback" ke kejadian asli yang dialamin bareng ("We won on Mossy Camp; we high-fived."). Mood-nya dial deterministik (bond, morale) yang naik-turun dari event. Alasan mood yang ngandung kata soal duit/belanja gak pernah ditampilin.

## Kenapa bagus
- Murah dan gak bisa halu: callback cuma ngutip fakta dari log match (`arena`, `won`, `choice`).
- Anti-repetisi: tiap sumber callback maksimal 3 "take" (`take` 0–2), ada jeda 3 hari antar callback, dan cuma ngambil kejadian 30 hari terakhir.
- Ada guard konsistensi: pilihan "hug/robbed/next_time" cuma dipake kalo kalah, "high_five/dance/told_you" kalo menang.
- Etis: regex `/\b(coins?|buy|bought|purchase\w*|price\w*|pay|paid|money|costs?|spend\w*|shop\w*|afford\w*|cheap|expensive|sale|deal)\b|[$€£₪]/i` ngebuang alasan mood yang nyebut duit. Companion gak bakal bilang "aku sedih kamu belum beli X". Ini guardrail anti dark pattern yang konkret.
- Ada sinyal "misses you" setelah 72 jam gak dibuka, tapi isinya cuma sapaan ("Saved you a spot."), bukan paksaan beli.

## Cara kerja
- `initialMood(now, history)` → dial awal dari jumlah match + level training.
- `moodView` → label per dial + `missesYou` (≥72 jam).
- `chooseCallback(sharedIncidents, callbackUses, day, tone)` → kalimat callback atau null.
- Teks akhir = sapaan(tone) + status(face) + alasan (kalo lolos filter duit) + callback.

## Cara pakai di project gw
- Pet/companion/AI friend: campur LLM dengan template deterministik yang nempel ke event log. Lebih murah, lebih konsisten, gak bisa ngarang kejadian.
- Pasang filter eksplisit biar persona gak pernah dipake buat jualan. Ini juga ngebantu kalo ada review app store/regulator soal manipulasi emosional.
- Simpan `callbackUses` biar persona gak ngulang cerita yang sama.

## Caveat / jangan ditiru
- Filter regex itu cuma bahasa Inggris (plus simbol mata uang). Butuh daftar per bahasa.
- Chat bebas (`/message`) tetap lewat LLM di server, dan guardrail di sana gak keliatan dari luar.

## Bukti
- Bundle publik: export `chooseCallback`, `readCallbackUses`, `initialMood`, `moodView`, plus regex filter duit di atas dalam modul yang sama.
