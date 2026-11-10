# good-tech

Database tech bagus yang gw temuin di project orang (atau project sendiri), buat referensi pas deploy project gw sendiri.

Satu file = satu tech. Kalau satu project punya 3 tech bagus, bikin 3 file.

## Struktur

| Folder | Isinya |
|---|---|
| `contracts/` | Smart contract: mekanik mint, PoW, bonding curve, hook, access gate, upgrade pattern |
| `backend/` | API, auth (SIWE, voucher, signature), queue, rate limit, DB design |
| `frontend/` | UX, wallet connect, bundle, real-time feed, mobile |
| `infra/` | Hosting, RPC, deploy pipeline, monitoring, supply-chain integrity |
| `security/` | Anti-bot, captcha, sybil filter, admin-key setup, audit trick |
| `data/` | Indexer, analytics, radar, scoring |
| `tokenomics/` | Price curve, fee split, reward/rent ke holder, supply schedule |

`_template.md` adalah template entry. `INDEX.md` digenerate otomatis, jangan diedit manual.

## Cara pakai

```bash
cd good-tech
python3 goodtech.py new contracts nama-project-nama-tech   # bikin entry dari template
python3 goodtech.py index                                   # rebuild INDEX.md
python3 goodtech.py list                                    # semua entry
python3 goodtech.py list --cat contracts --tag pow          # filter
python3 goodtech.py search "state override"                 # cari full-text
```

## Kolaborasi (repo private)

```bash
git clone <url-repo>
cd good-tech
git config core.hooksPath .githooks       # sekali aja: lint otomatis tiap commit
python3 goodtech.py new backend nama-project-nama-tech
# isi file-nya, lalu:
python3 goodtech.py index && python3 goodtech.py lint
git add -A && git commit -m "add: <project> <tech>" && git push
```

- Satu entry = satu commit biar gampang di-review.
- Repo ini **public**. `lint` nolak link ke catatan pribadi (`[[...]]`), path folder lokal (`*-recon/`, folder bot), apapun yang mirip secret, dan kalimat soal operasi/relasi pribadi. Commit ditolak kalau lint gagal.
- Jangan tulis nama orang dari tim anon (ganti `<A>`/`<B>`), dan jangan tulis wallet/hasil mint/profit pribadi.
- Bukti yang nunjuk file lokal ditulis "snapshot recon" / "laporan recon internal". Kalau ada sumber publik (explorer, repo, URL), pakai itu.

## Aturan isi

- **Status jujur.** `verified` = udah gw cek sendiri (on-chain, fork, baca kode). `claimed` = baru klaim docs/tim. `idea` = belum ada yang implement, baru ide gw.
- **Skor 1-10** = seberapa layak ditiru, bukan seberapa bagus projectnya. Project rug bisa punya tech 9/10.
- **Selalu isi "Caveat".** Tiap tech ada jebakannya; itu yang paling berguna pas deploy.
- **Bukti wajib.** Tx hash, address contract, path file kode, atau link. Kalau gak ada bukti, statusnya `claimed`.
- **Jangan taruh secret.** Gak ada private key, seed, API key, atau `.env` di folder ini.
- Pas recon/audit project baru, kalau ada tech yang bagus, langsung bikin entry di sini.
