#!/usr/bin/env python3
"""Interactive script to create add-in entries for the pancalc registry.

Walks through questions, calculates SHA256, and outputs the JSON
ready for submission to the registry.

Usage:
    python tools/make_addin.py
    python tools/make_addin.py -o addins/myaddin.json
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path


def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ask(prompt: str, default: str | None = None, required: bool = False) -> str:
    if default is not None:
        answer = input(f"  {prompt} [{default}]: ").strip()
        return answer if answer else default
    answer = input(f"  {prompt}: ").strip()
    if required and not answer:
        print("  !! This field is required.")
        return ask(prompt, default, required)
    return answer


def ask_validated(prompt: str, validator, default: str | None = None, required: bool = False) -> str:
    while True:
        value = ask(prompt, default, required)
        if not value and not required:
            return value
        error = validator(value)
        if error:
            print_warn(error)
        else:
            return value


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    options = "Y/n" if default else "y/N"
    answer = input(f"  {prompt} [{options}]: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def print_header(title: str):
    print(f"\n  {'=' * 56}")
    print(f"  {title}")
    print(f"  {'=' * 56}")


def print_ok(msg: str):
    print(f"  [OK] {msg}")


def print_warn(msg: str):
    print(f"  [!] {msg}")


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def validate_id(value: str) -> str | None:
    if not re.match(r'^[a-z0-9][a-z0-9-]*$', value):
        return "ID must be lowercase, start with a letter/digit, and contain only hyphens (no spaces, no uppercase)."
    if value != value.lower():
        return "ID must be lowercase."
    return None


def validate_url(value: str) -> str | None:
    if not value.startswith(("http://", "https://")):
        return "URL should start with https:// (or http://)."
    return None


def validate_filename(value: str) -> str | None:
    if "." not in value:
        return "Filename should have an extension (e.g. .g3a, .ac2)."
    if re.search(r'[\s]', value):
        return "Filename contains spaces. Calculator cannot read these."
    return None


def choose_category() -> str:
    categories = ["math", "utilities", "emulators", "education"]
    print(f"  Available categories: {', '.join(categories)}")
    cat = ask("Category").lower()
    if cat not in categories:
        if not ask_yes_no(f"  '{cat}' is not a standard category. Continue?"):
            return choose_category()
    return cat


def ask_filepath(prompt: str, required: bool = True) -> Path:
    while True:
        value = ask(prompt, required=required)
        if not value and not required:
            return Path()
        p = Path(value)
        if not p.exists():
            print_warn(f"File not found: {p}")
            continue
        return p


def ask_url(prompt: str, *, required: bool = False) -> str:
    while True:
        url = ask(prompt, required=required)
        if not url and not required:
            return url
        err = validate_url(url)
        if err:
            if not ask_yes_no(f"{err} Continue anyway?"):
                continue
        return url


# ---------------------------------------------------------------------------
# File info collection
# ---------------------------------------------------------------------------

def collect_file_info(
    file_num: int, total_files: int | None = None, addin_id: str | None = None
) -> tuple[dict, Path]:
    """Ask about one file entry. Returns (entry_dict, local_path)."""
    if total_files:
        print()
        print(f"  --- File {file_num} of {total_files} (for add-in '{addin_id or '?'}') ---")
        print(f"      All {'these' if total_files > 1 else 'this'} file{'s' if total_files > 1 else ''} belong to the SAME add-in.")
        print(f"      Give each file a unique name (e.g. 'myaddin.g3a', 'myaddin.ac2').")
    else:
        print()

    filename = ask_validated("Filename on calculator", validate_filename, required=True)
    local_path = ask_filepath("Path to local file for SHA256")
    sha256 = sha256_file(str(local_path))
    print_ok(f"SHA256: {sha256}")

    download_type = ask("Download type", default="direct")

    entry: dict = {
        "filename": filename,
        "download_url": ask_url("Download URL", required=True),
        "download_type": download_type,
        "sha256": sha256,
    }

    if download_type == "zip":
        entry["zip_file"] = ask("Filename inside zip", default=filename)

    return entry, local_path


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_addin() -> dict:
    print_header("Add-in Metadata")

    addin_id = ask_validated("Add-in ID (slug, e.g. 'myaddin')", validate_id, required=True)
    name = ask("Name (human-readable)", required=True)
    author = ask("Author", required=True)
    version = ask("Version", default="1.0")
    description = ask("Description", required=True)
    category = choose_category()

    compatible_raw = ask("Compatible models (comma-separated)", default="fx-CG50")
    compatible = [m.strip() for m in compatible_raw.split(",") if m.strip()]

    url = ask_url("Project URL")
    license_val = ask("License", default="unknown")

    tags_raw = ask("Tags (comma-separated)")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    print_header("File Structure")
    is_multi = ask_yes_no("Multi-file add-in (multiple downloadable files)?")

    files_entries: list[dict] = []
    total_size = 0

    if is_multi:
        num_str = ask("Number of files", default="2")
        try:
            num_files = int(num_str)
        except ValueError:
            num_files = 2
        for i in range(num_files):
            entry, local_path = collect_file_info(i + 1, total_files=num_files, addin_id=addin_id)
            files_entries.append(entry)
            total_size += local_path.stat().st_size
    else:
        print("  (single file)")
        local_path = ask_filepath("Path to local file for SHA256")
        sha256 = sha256_file(str(local_path))
        print_ok(f"SHA256: {sha256}")

        total_size = local_path.stat().st_size

        download_type = ask("Download type", default="direct")
        download_url = ask_url("Download URL", required=True)

        entry: dict = {
            "filename": local_path.name,
            "download_url": download_url,
            "download_type": download_type,
            "sha256": sha256,
        }

        if download_type == "zip":
            entry["zip_file"] = ask("Filename inside zip", default=f"{addin_id}.g3a")

        files_entries.append(entry)

    # --- Build add-in dict ---
    addin: dict = {
        "id": addin_id,
        "name": name,
        "author": author,
        "version": version,
        "description": description,
        "category": category,
        "compatible": compatible,
        "url": url if url.startswith(("http://", "https://")) else f"https://{url}" if url else "",
        "size_kb": round(total_size / 1024, 1),
        "license": license_val,
        "tags": tags,
    }

    if is_multi:
        addin["files"] = files_entries
    else:
        e = files_entries[0]
        addin["download_url"] = e["download_url"]
        addin["download_type"] = e["download_type"]
        addin["sha256"] = e["sha256"]
        if e.get("zip_file"):
            addin["zip_file"] = e["zip_file"]

    return addin


def print_json(addin: dict, output_path: str | None = None):
    if output_path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(addin, f, indent=2)
        print_ok(f"Saved to: {p}")

    print_header("Generated Add-in JSON")
    print(json.dumps(addin, indent=2))
    print()

    print(f"  *** Next steps:")
    print(f"       1. Fork the registry: https://github.com/pan-devs/pancalc-registry")
    print(f"       2. Save this JSON to addins/{addin['id']}.json")
    print(f"       3. Add '{addin['id']}.json' to registry.json's addins list")
    print(f"       4. Open a Pull Request")
    print(f"       Pan Devs will review, test, and GPG-sign the add-in.")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Create add-in entries for the pancalc registry"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save JSON to file (e.g. addins/myaddin.json)",
    )
    args = parser.parse_args()

    print()
    print(f"  {'=' * 56}")
    print(f"  PanCalc Registry Add-in Creator")
    print(f"  {'=' * 56}")

    addin = build_addin()
    print_json(addin, args.output)


if __name__ == "__main__":
    main()
