# Contributing to PanCalc Registry

The PanCalc registry is the central index of add-ins for the Casio fx-CG50 and fx-CG100.
Anyone can submit an add-in via Pull Request — Pan Devs reviews and signs approved entries.

---

## Quick way (recommended)

Use the interactive helper script:

```bash
python tools/make_addin.py -o addins/myaddin.json
```

It will ask you questions about your add-in, calculate the SHA256 hash of your file,
and generate a ready-to-submit JSON. Then:

1. **Fork** the registry on GitHub
2. Add your JSON file to `registry.json`'s `addins` list
3. Open a Pull Request

## Manual way

1. **Fork** this repository
2. **Create a new JSON file** under `addins/` named after your add-in ID (e.g. `addins/myaddin.json`)
3. **Fill in the schema** (see below)
4. **Add your entry** to the `addins` array in `registry.json`
5. **Open a Pull Request** with a short description

Pan Devs will review the PR, test the add-in, and if approved, sign the file(s)
with the Pan Devs GPG key and merge.

---

## Add-in JSON schema

### Single-file add-in (most common)

```json
{
  "id": "myaddin",
  "name": "My Add-in",
  "author": "Your Name",
  "version": "1.0",
  "description": "What this add-in does",
  "category": "utilities",
  "compatible": ["fx-CG50", "fx-CG100"],
  "url": "https://example.com/myaddin",
  "download_url": "https://example.com/files/myaddin.g3a",
  "download_type": "direct",
  "sha256": "abc123...",
  "size_kb": 240.5,
  "license": "GPL-3.0",
  "tags": ["tag1", "tag2"]
}
```

### Multi-file add-in (e.g. KhiCAS)

```json
{
  "id": "khicas",
  "name": "KhiCAS",
  "author": "Author",
  "version": "latest",
  "description": "Description",
  "category": "math",
  "compatible": ["fx-CG50"],
  "url": "https://example.com/khicas",
  "size_kb": 4300.8,
  "license": "GPL-3.0",
  "tags": ["cas", "math", "python"],
  "files": [
    {
      "filename": "khicas50.g3a",
      "download_url": "https://example.com/khicas50.g3a",
      "download_type": "direct",
      "sha256": "2f60d1d8..."
    },
    {
      "filename": "khicas50.ac2",
      "download_url": "https://example.com/khicas50.ac2",
      "download_type": "direct",
      "sha256": "fdfa78e7..."
    }
  ]
}
```

### Zip file add-in (e.g. Nesizm)

```json
{
  "id": "nesizm",
  "name": "Nesizm",
  "author": "Author",
  "version": "1.00",
  "description": "Description",
  "category": "emulators",
  "compatible": ["fx-CG50"],
  "url": "https://example.com/nesizm",
  "download_url": "https://example.com/nesizm_v1.0.zip",
  "download_type": "zip",
  "zip_file": "nesizm.g3a",
  "sha256": "9dc94ba5...",
  "size_kb": 239.6,
  "license": "MIT",
  "tags": ["nes", "emulator", "retro", "games"]
}
```

### `download_type` values

| Value | Description |
|-------|-------------|
| `direct` | The `.g3a` is hosted somewhere (ideally the registry's `files/`). |
| `zip` | Link to a `.zip` file containing the `.g3a`. Requires `zip_file`. |

### Game / Emulator add-in (e.g. NES, GB, GBA ROMs)

The registry does **not** host copyrighted ROMs (see [Guidelines](#guidelines)).
The only hosted game is `test_rom` — a mock 21-byte placeholder that documents
the schema, never a real game ("do not download"). Use its shape as a template:

```json
{
  "id": "test_rom",
  "name": "Test ROM — do not download",
  "author": "Pan Devs",
  "version": "1.0",
  "description": "Mock/test entry that demonstrates the game schema of the registry. This is NOT a real game.",
  "category": "games",
  "compatible": ["fx-CG50"],
  "url": "https://github.com/pan-devs/pancalc-registry",
  "download_url": "https://raw.githubusercontent.com/pan-devs/pancalc-registry/main/files/test.nes",
  "download_type": "direct",
  "sha256": "9512e50d289ed2c29e89a6ebb9524ed8c1b98b244aa7f9d3f84e9138dbd6f670",
  "filename": "test.nes",
  "size_kb": 0.02,
  "license": "unknown",
  "tags": ["test", "example", "nes", "emulator", "games"],
  "emulator": "nesizm",
  "platform": "NES"
}
```

**Required game-specific fields:**
- `category` must be `"games"`
- `emulator` — emulator add-in ID (e.g. `nesizm`, `gpsp`, `smsplusgx`)
- `platform` — original platform name (e.g. `NES`, `GB`, `GBA`, `SMS`, `GG`)
- `filename` — exact filename on calculator (sanitized, no spaces)

**Notes:**
- `download_type` is always `"direct"` (no zip for game ROMs)
- ROMs are hosted in the registry's `files/` directory
- SHA256 is computed from the ROM file
- Games appear in the `games/` subdirectory and `registry.json`'s `games` array
- `pcalc games list` / `pcalc games install <id>` from PanCalc Tools

**ROM policy:**
- The registry hosts **no copyrighted ROMs**. Each contributor is responsible
  for the files they reference — only submit ROMs you are authorised to
  redistribute (public domain, freely licensed, or homebrew with permission).
- Prefer linking to the original/official download instead of re-hosting a copy.
- Sanity-check: if a game could be confused with a pirated ROM, leave it out.

### Required fields

- `id` — unique, lowercase, hyphens only
- `name` — display name
- `author` — author or maintainer
- `version` — current version string
- `description` — short description of what the add-in does
- `category` — one of: `utilities` | `math` | `emulators` | `education` | `games`
- `compatible` — list of compatible calculator models
- `url` — homepage or source repository
- `download_url` (single-file) or `files[]` (multi-file) — download location
- `download_type` — see table above
- `sha256` — SHA256 hex digest of the downloaded file
- `license` — SPDX identifier if known, `"unknown"` otherwise

### Optional fields

- `zip_file` — filename of the `.g3a` inside the zip (required when `download_type` is `zip`)
- `size_kb` — approximate file size in KiB
- `tags` — searchable keywords
- `signature_url` — GPG signature URL, filled by Pan Devs after approval
- `files` — array of file entries (replaces `download_url`/`download_type`/`sha256` for multi-file add-ins)

---

## GPG verification

All add-ins approved by Pan Devs are signed with the Pan Devs GPG key.

**Key ID:** `1A370E1B68A194A8`
**Fingerprint:** `C7AD 9689 E894 B261 7EAB CFE2 1A37 0E1B 68A1 94A8`
**Public key:** [`pandevs.asc`](./pandevs.asc) — also available at [keys.openpgp.org](https://keys.openpgp.org)

Signatures (`.asc` files) are published alongside each file in the `files/` directory.
`pcalc verify <addin>` checks both SHA256 and the GPG signature automatically.

---

## Guidelines

- Only submit add-ins that work on the fx-CG50 or fx-CG100
- The add-in must be publicly available (free download, no login required)
- Official add-ins (e.g. from Casio's website) are welcome — link to the official source, do not redistribute the binary
- **No copyrighted ROMs.** The registry hosts no ROMs for commercial games
  (NES, GB, GBA, SMS, GG, etc.). The only hosted game is the `test_rom` mock —
  contributors are responsible for the files they add, and should only reference
  freely redistributable content.
- No malware, no obfuscated binaries without source
- If the license is unknown, set `"license": "unknown"` — don't guess
- One add-in per PR
- Use the `tools/make_addin.py` script to generate your JSON and avoid mistakes

> **Note (emulators):** a Game Boy Advance emulator port (`gpsp-sh4-jit`, by
> KaraRyougi) is a **candidate** for the registry. It is not accepted yet — it
> still needs review, license verification (gpSP is GPL-2.0), and signing by Pan
> Devs before it can be submitted here.
