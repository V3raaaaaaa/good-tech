# good-tech index

Digenerate oleh `python3 goodtech.py index`. Jangan edit manual.

Total: 34 entry

## contracts

| Skor | Tech | Project | Status | Tags |
|---|---|---|---|---|
| 9 | [Launch coin + fee split permanen dalam satu Jito bundle](contracts/forkswiki-atomic-locked-fee-split-launch.md) | forks.wiki | verified | launchpad, pump-fun, fee-share, jito, bundle, github, non-custodial |
| 8 | [On-chain keccak PoW mint (burst difficulty)](contracts/hashcats-onchain-keccak-pow-mint.md) | Hashcats (hashcats.fun) | verified | pow, mint, nft, difficulty, no-backend |
| 8 | [Claim vault voucher EIP-712 + cap harian per wallet & global on-chain](contracts/tinylegends-claim-vault-voucher-daily-caps.md) | Tiny Legends | verified | p2e, voucher, eip712, claim, rate-limit, hot-key, game-economy |
| 8 | [LP graduation full-range dikunci di locker tanpa fungsi remove](contracts/vibevibe-full-range-lp-locker-no-remove.md) | vibe/vibe (Seedify) | verified | uniswap-v4, lp-lock, graduation, anti-rug, immutable |
| 8 | [Transfer token dikunci sampai graduate + allowlist venue](contracts/vibevibe-transfer-lock-venue-allowlist.md) | vibe/vibe (Seedify) | verified | launchpad, bonding-curve, anti-sniper, anti-rug, erc20, uniswap-v4 |
| 7 | [PoW mint dengan domain-separated digest + maxPrice + 1 mint/block](contracts/unicred-pow-maxprice-anchor-window.md) | UNICRED (unicred.fun) | verified | pow, mint, nft, slippage, uniswap-v4 |
| 7 | [Tax token yang dikonfigurasi creator lewat hook Uniswap v4 (cash/reflection/burn/pair)](contracts/vibevibe-v4-hook-creator-tax-weights.md) | vibe/vibe (Seedify) | verified | uniswap-v4, hook, tax, reflection, buyback, tokenomics, launchpad |
| 6 | [NFT reveal pakai block delay + offset, dan perk berdasarkan lama hold (heldSince)](contracts/tinylegends-founders-delayed-reveal-heldsince.md) | Tiny Legends (Founders NFT) | claimed | nft, reveal, randomness, holding-perk, erc721 |
| 6 | [Treasury yang otomatis split tiap pembayaran ke burn + reward pool](contracts/tinylegends-treasury-auto-split-burn-rewards.md) | Tiny Legends | verified | treasury, fee-split, burn, reward-pool, sink, game-economy |

## backend

| Skor | Tech | Project | Status | Tags |
|---|---|---|---|---|
| 8 | [LLM ngusulin, API resmi yang verifikasi (1 call, cache per pertanyaan)](backend/forkswiki-llm-proposes-github-verifies.md) | forks.wiki | verified | llm, verification, github, graphql, cache, cost |
| 8 | [Ticket stateless (HMAC + AES-GCM) antar step multi-request](backend/forkswiki-stateless-signed-tickets.md) | forks.wiki | verified | serverless, hmac, aes-gcm, stateless, session, security |
| 8 | [Sync game pakai intent + claim, ledger ekonomi di server, txid idempotent + versi](backend/sindicat-intent-claim-server-ledger.md) | SINDICAT | verified | game, server-authoritative, anti-cheat, sync, idempotency, optimistic-concurrency |
| 7 | [Respons API indexer yang jujur soal freshness (asOfBlock + lag + coverage)](backend/vibevibe-indexer-freshness-envelope.md) | vibe/vibe (Seedify) | verified | indexer, api-design, freshness, pagination, reorg |
| 6 | [Cloud save offline-first dengan merge berdasarkan progress + optimistic concurrency (409 stale)](backend/tinylegends-cloud-save-progress-merge.md) | Tiny Legends | verified | game, save-sync, offline-first, concurrency, siwe |
| 6 | [Remote config live dengan skema min/max/type + endpoint harga ber-flag stale](backend/tinylegends-remote-config-bounded-overrides.md) | Tiny Legends | verified | remote-config, live-ops, feature-flags, oracle, game-economy |

## frontend

| Skor | Tech | Project | Status | Tags |
|---|---|---|---|---|
| 6 | [Codex aturan dengan angka asli game + landing pakai klip gameplay hover-to-play](frontend/sindicat-codex-and-filmed-landing.md) | SINDICAT | verified | docs, transparency, landing-page, onboarding, trust |
| 6 | [Boot SPA bertahap: inline script prefetch data pertama + modulepreload dari manifest build](frontend/vibevibe-staged-prestart-boot.md) | vibe/vibe (Seedify) | verified | performance, lcp, vite, modulepreload, prefetch, spa |
| 5 | [Komentar kode yang nyatet tanggal + siapa yang mutusin + varian yang dipilih](frontend/sindicat-dated-decision-comments.md) | SINDICAT | verified | dev-process, documentation, design-decisions, ai-assisted-dev |
| 5 | [Loading screen inline yang mirip game, digambar sebelum bundle 2.5 MB datang](frontend/tinylegends-inline-loader-before-bundle.md) | Tiny Legends | verified | performance, perceived-speed, web-game, mobile, loading |

## infra

| Skor | Tech | Project | Status | Tags |
|---|---|---|---|---|
| 7 | [Client engine di-pin pakai sha256 + client-side vault](infra/ordropz-sha256-pinned-client-engine.md) | Ord Dropz (shielded Ordinals launchpad) | verified | supply-chain, integrity, esm, client-side, psbt |
| 7 | [Deploy immutable per "run" + frontend pin runtime hash bytecode](infra/vibevibe-immutable-runs-runtime-hash-pin.md) | vibe/vibe (Seedify) | verified | deployment, immutable, versioning, integrity, frontend-config |
| 6 | [Pool vanity mint address (…fork) di-grind duluan](infra/forkswiki-vanity-mint-key-pool.md) | forks.wiki | verified | vanity, branding, keypair, solana, launchpad |
| 6 | [Server game multi-region dengan /health yang ngelaporin commit, region, DB, dan status config auth](infra/sindicat-multi-region-health-endpoint.md) | SINDICAT | verified | multi-region, health-check, observability, railway, deployment |

## security

| Skor | Tech | Project | Status | Tags |
|---|---|---|---|---|
| 7 | [Buyback oleh keeper dengan batas on-chain + ganti treasury 2 langkah](security/vibevibe-keeper-buyback-onchain-limits.md) | vibe/vibe (Seedify) | verified | keeper, buyback, burn, timelock, treasury, admin-limits |
| 6 | [Filter ticker/nama anti-impersonation (homoglyph + leet + fonetik)](security/forkswiki-homoglyph-ticker-filter.md) | forks.wiki | verified | impersonation, homoglyph, filter, launchpad, anti-scam |
| 6 | [Early access "citizenship": waitlist referral + wallet + kode, batas akun per device, guest session](security/sindicat-early-access-citizenship-gate.md) | SINDICAT | verified | early-access, waitlist, sybil, referral, privy, gating |
| 6 | [Tiket fight dari server + durasi minimum sebelum hasil diterima (anti-cheat ringan)](security/tinylegends-fight-ticket-min-duration.md) | Tiny Legends | verified | anti-cheat, game, p2e, rate-limit, server-ticket |

## data

| Skor | Tech | Project | Status | Tags |
|---|---|---|---|---|
| 8 | [Mint recipe dari tx sukses + replay eth_call dengan state override](data/mintradar-recipe-replay-state-override.md) | Mint Radar (punya sendiri) | verified | indexer, eth_call, state-override, recon, automation |
| 7 | [Sinyal radar mint (deployer record, two-phase, timed, 72h outcome)](data/agenticmint-radar-signals.md) | agenticmint.ai (Dr.OVG) | verified | radar, scoring, deployer, analytics |

## tokenomics

| Skor | Tech | Project | Status | Tags |
|---|---|---|---|---|
| 7 | [Heat + laundering: risiko pegang cash dan exit token yang dipersempit lewat "front business"](tokenomics/sindicat-heat-laundering-exit-throttle.md) | SINDICAT | verified | game-economy, outflow-control, emission, sink, lore-driven-design, p2e |
| 7 | [Poin harian dipatok USD, dibayar dari pool harian pro-rata ("never pays more than the pool holds")](tokenomics/tinylegends-daily-pool-prorata-points.md) | Tiny Legends | verified | p2e, reward-pool, oracle, pro-rata, emission-control, game-economy |
| 6 | [Rent ke holder epoch sebelumnya](tokenomics/hashcats-rent-to-earlier-holders.md) | Hashcats (hashcats.fun) | verified | nft, revenue-share, epoch, price-curve |
| 6 | [Fee withdraw yang turun tiap hari nunggu + hold rule anti-dump](tokenomics/tinylegends-decaying-withdraw-fee-hold-rule.md) | Tiny Legends | verified | p2e, withdraw-fee, anti-dump, anti-bot, vesting |
| 5 | [Harga launch window terbatas + progress offline dengan cap dan efisiensi](tokenomics/tinylegends-launch-window-offline-cap.md) | Tiny Legends | verified | game-design, idle, launch-pricing, retention, fomo |
