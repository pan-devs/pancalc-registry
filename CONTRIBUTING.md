# Contributing to PanCalc Registry

The PanCalc registry is the central index of add-ins for the Casio fx-CG50 and fx-CG100.
Anyone can submit an add-in via Pull Request — Pan Devs reviews and signs approved entries.

---

## How to submit an add-in

1. **Fork** this repository
2. **Create a new JSON file** under `addins/` named after your add-in ID (e.g. `addins/myaddin.json`)
3. **Fill in the schema** (see below)
4. **Add your entry** to the `addins` array in `registry.json`
5. **Open a Pull Request** with a short description

Pan Devs will review the PR, test the add-in, and if approved, sign the `.g3a` with the Pan Devs GPG key and merge.

---

## Add-in JSON schema

```json
{
  "id": "unique-lowercase-id",
  "name": "Display Name",
  "author": "Author Name",
  "version": "1.0",
  "description": "What it does, in 1-2 sentences.",
  "category": "utilities | math | games | emulators | education | dev | other",
  "compatible": ["fx-CG50", "fx-CG100"],
  "url": "https://github.com/author/repo",
  "download_url": "https://direct.link/to/file.g3a",
  "size_kb": 123,
  "license": "MIT | GPL-3.0 | GPL-2.0 | ...",
  "tags": ["tag1", "tag2"]
}
```

### Required fields
- `id` — unique, lowercase, hyphens only
- `name` — display name
- `author` — author or maintainer
- `version` — current version string
- `description` — short description
- `category` — one of the values above
- `compatible` — list of compatible models
- `url` — homepage or source repo
- `download_url` — direct link to the `.g3a` file
- `license` — SPDX identifier if known, `"unknown"` otherwise

### Optional fields
- `size_kb` — file size in KiB (integer), `null` if unknown
- `tags` — searchable keywords

---

## GPG verification

All add-ins approved by Pan Devs are signed with the Pan Devs GPG key.

**Key ID:** `1A370E1B68A194A8`  
**Fingerprint:** `C7AD 9689 E894 B261 7EAB CFE2 1A37 0E1B 68A1 94A8`  
**Public key:** [`pandevs.asc`](./pandevs.asc) — also available at [keys.openpgp.org](https://keys.openpgp.org)

Signatures (`.sig` files) are published alongside each `.g3a` in GitHub Releases.
`pcalc verify <addin>` checks both SHA256 and the GPG signature automatically.

---

## Guidelines

- Only submit add-ins that work on the fx-CG50 or fx-CG100
- The add-in must be publicly available (free download, no login required)
- No malware, no obfuscated binaries without source
- If the license is unknown, set `"license": "unknown"` — don't guess
- One add-in per PR
