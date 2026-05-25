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
  "id": "",
  "name": "",
  "author": "",
  "version": "",
  "description": "",
  "category": "",
  "compatible": ["fx-CG50", "fx-CG100"],
  "url": "",
  "download_url": "",
  "download_type": "direct | g3a | zip",
  "zip_file": "(only if download_type is zip)",
  "sha256": "",
  "size_kb": null,
  "license": "",
  "tags": [],
  "signature_url": "(only if download_type is direct — filled by Pan Devs)"
}
```

### `download_type` values

| Value | Description |
|-------|-------------|
| `direct` | The `.g3a` is hosted in this registry under `files/`. Used for add-ins Pan Devs mirrors directly. |
| `g3a` | Direct link to a `.g3a` file hosted externally. |
| `zip` | Link to a `.zip` file containing the `.g3a`. Requires `zip_file` field. |

### Required fields

- `id` — unique, lowercase, hyphens only
- `name` — display name
- `author` — author or maintainer
- `version` — current version string
- `description` — short description of what the add-in does
- `category` — one of: `utilities` | `math` | `games` | `emulators` | `education` | `dev` | `other`
- `compatible` — list of compatible models
- `url` — homepage or source repository
- `download_url` — link to the `.g3a` or `.zip` file
- `download_type` — see table above
- `license` — SPDX identifier if known, `"unknown"` otherwise

### Optional fields

- `zip_file` — filename of the `.g3a` inside the zip (required when `download_type` is `zip`)
- `size_kb` — file size in KiB, `null` if unknown
- `tags` — searchable keywords
- `signature_url` — GPG signature URL, filled by Pan Devs after approval (only for `direct` type)

> **Note:** Leave `sha256` empty — it will be calculated and verified by Pan Devs during review.

---

## GPG verification

All add-ins approved by Pan Devs are signed with the Pan Devs GPG key.

**Key ID:** `1A370E1B68A194A8`  
**Fingerprint:** `C7AD 9689 E894 B261 7EAB CFE2 1A37 0E1B 68A1 94A8`  
**Public key:** [`pandevs.asc`](./pandevs.asc) — also available at [keys.openpgp.org](https://keys.openpgp.org)

Signatures (`.asc` files) are published alongside each `.g3a` in the `files/` directory.  
`pcalc verify <addin>` checks both SHA256 and the GPG signature automatically.

---

## Guidelines

- Only submit add-ins that work on the fx-CG50 or fx-CG100
- The add-in must be publicly available (free download, no login required)
- Official add-ins (e.g. from Casio's website) are welcome — link to the official source, do not redistribute the binary
- No malware, no obfuscated binaries without source
- If the license is unknown, set `"license": "unknown"` — don't guess
- One add-in per PR