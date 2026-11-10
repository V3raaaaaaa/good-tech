---
name: Installer asset yang validasi isi zip dengan ketat (allowlist nama file + manifest + atomic replace)
category: security
project: Weird Cats
chain: -
tags: [installer, zip, path-traversal, supply-chain, python, codex-plugin]
score: 6
status: verified
added: 2026-11-11
source: recon 2026-11-11, https://github.com/nett0eth/weird-cats-codex-pets/blob/HEAD/plugins/weird-cats/scripts/install_pet.py
---
# Installer asset yang validasi isi zip dengan ketat

## Ringkas
Script Python ~70 baris yang install "pet" (zip berisi `pet.json` + `spritesheet.webp`) ke folder user. Isi zip dicek super ketat sebelum ditulis: daftar file harus persis 2 nama itu, id harus cocok regex, manifest harus cocok id, sprite harus beneran WebP, tulis lewat file `.tmp` lalu `os.replace`, dan nolak nimpa folder milik pet lain.

## Kenapa bagus
- Kebal zip-slip / path traversal: gak pernah `extractall`, cuma baca 2 member yang namanya udah fix.
- Kebal file nyusup (executable, symlink, dotfile): kalau `namelist()` beda sedikit aja, abort.
- Atomic: kalau proses mati di tengah, file lama tetap utuh.
- Gak ngerusak data user lain: folder dengan `pet.json` ber-`id` beda ditolak.
- Gak ada network call, gak ada `subprocess`/`eval`. Semua asset udah ikut di repo.

## Cara kerja
```python
if not re.fullmatch(r'weird-cats-[a-z0-9-]+', pet_id): abort
if Path(archive_name).name != archive_name or not archive_name.endswith('.zip'): abort
with zipfile.ZipFile(archive) as z:
    if set(z.namelist()) != {'pet.json', 'spritesheet.webp'} or z.testzip(): abort
    manifest, sprite = z.read('pet.json'), z.read('spritesheet.webp')
m = json.loads(manifest)
if m['id'] != pet_id or m['spriteVersionNumber'] != 2 or m['spritesheetPath'] != 'spritesheet.webp': abort
if not sprite.startswith(b'RIFF') or b'WEBP' not in sprite[:16]: abort
# existing folder dengan id lain -> abort
for name, data in files: write(name + '.tmp'); os.replace(tmp, name)
```
Catalog (`assets/catalog.json`) juga dicek jumlahnya (harus 25) dan nama unik.

## Cara pakai di project gw
- Pola ini cocok buat apa pun yang install "content pack" user-generated atau dari repo: skin, theme, plugin data, model config, airdrop asset.
- Ganti `set(namelist()) == {...}` dengan allowlist yang sesuai; tambah batas ukuran per member (`ZipInfo.file_size`) biar kebal zip bomb.
- Magic-byte check per tipe file (PNG `\x89PNG`, WebP `RIFF....WEBP`, JSON parse).
- Tambah `--destination` buat testing, kayak script aslinya.

## Caveat / jangan ditiru
- Validasi ini gak ngelindungin kalau repo-nya sendiri dibobol (script-nya juga ikut diganti). Pin ke commit/tag dan publikasi hash release.
- Repo sebelah dari project yang sama (Plush Pets) malah pakai `curl .../main/install.sh | sh` dan `irm ... | iex` dari branch `main` yang gak di-pin. Itu yang JANGAN ditiru.
- Gak ada limit ukuran file di script aslinya.

## Bukti
- https://github.com/nett0eth/weird-cats-codex-pets/blob/HEAD/plugins/weird-cats/scripts/install_pet.py (fungsi `install`, `load_catalog`)
- https://github.com/nett0eth/weird-cats-codex-pets/blob/HEAD/plugins/weird-cats/skills/weird-cats/SKILL.md (skill Codex yang manggil script)
- Kontras: https://github.com/nett0eth/weird-cats-plush-pets/blob/HEAD/install/install.sh baris 5, 61 (pipe-to-shell dari `main`)
