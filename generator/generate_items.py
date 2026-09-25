#!/usr/bin/env python3
"""
All Items – Generator für den Item-Pool.

Lädt die offizielle Item-Registry einer Minecraft-Version (über das
Projekt "misode/mcmeta", das die Daten direkt aus dem Vanilla-Client
extrahiert), filtert die Einträge aus exclusions.txt heraus und erzeugt:

  * datapack/data/allitems/function/internal/pool.mcfunction
      -> füllt beim Spielstart die Command Storage mit allen Items
  * generator/item_list.txt
      -> lesbare Liste aller Items im Pool (ID + deutscher Name)
  * datapack/pack.mcmeta
      -> pack_format / min_format / max_format passend zur Version

Bei einem Versionswechsel einfach mit der neuen Version erneut ausführen:

    python3 generator/generate_items.py --version 26.4

Nur Python-Standardbibliothek, keine zusätzlichen Pakete nötig.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR_DIR = ROOT / "generator"
DATAPACK_DIR = ROOT / "datapack"
POOL_FILE = DATAPACK_DIR / "data" / "allitems" / "function" / "internal" / "pool.mcfunction"
PACK_MCMETA = DATAPACK_DIR / "pack.mcmeta"
ITEM_LIST_FILE = GENERATOR_DIR / "item_list.txt"
EXCLUSIONS_FILE = GENERATOR_DIR / "exclusions.txt"

MCMETA = "https://raw.githubusercontent.com/misode/mcmeta"
PACK_DESCRIPTION = "All Items – sammle jedes Item im Spiel!"


def fetch_json(url: str):
    """Lädt eine JSON-Datei per HTTPS."""
    print(f"  lade {url}")
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)


def load_exclusions(path: Path) -> list[str]:
    """Liest die Ausschlussliste (ein Muster pro Zeile, '#' = Kommentar)."""
    patterns = []
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = line.split("#", 1)[0].strip()
        if entry:
            patterns.append(entry.removeprefix("minecraft:"))
    return patterns


def pack_format_for(version: str) -> tuple[int, int]:
    """Sucht das Datapack-Format (Haupt- und Nebenversion) der angegebenen Version."""
    versions = fetch_json(f"{MCMETA}/refs/heads/summary/versions/data.json")
    for v in versions:
        if v["id"] == version:
            return int(v["data_pack_version"]), int(v.get("data_pack_version_minor", 0))
    sys.exit(f"Fehler: Version '{version}' ist in mcmeta nicht bekannt.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Erzeugt den Item-Pool für das All-Items-Datapack.")
    parser.add_argument("--version", default="26.3", help="Minecraft-Version (Standard: 26.3)")
    args = parser.parse_args()
    version = args.version

    print(f"Minecraft {version}")
    registry = fetch_json(f"{MCMETA}/{version}-registries/item/data.json")
    components = fetch_json(f"{MCMETA}/{version}-summary/item_components/data.json")
    lang_de = fetch_json(f"{MCMETA}/{version}-assets-json/assets/minecraft/lang/de_de.json")
    pack_format = pack_format_for(version)

    # --- Ausschlüsse anwenden --------------------------------------------
    patterns = load_exclusions(EXCLUSIONS_FILE)
    unused = set(patterns)
    pool = []
    for item in sorted(registry):
        hits = [p for p in patterns if fnmatch.fnmatchcase(item, p)]
        unused -= set(hits)
        if not hits:
            pool.append(item)
    for p in sorted(unused):
        print(f"  Hinweis: Ausschluss '{p}' passt auf kein Item dieser Version.")

    # --- Übersetzungsschlüssel ermitteln ---------------------------------
    # Der Schlüssel (z.B. "item.minecraft.diamond" oder "block.minecraft.stone")
    # wird im Spiel automatisch in die Sprache des Spielers übersetzt.
    entries = []
    for item in pool:
        name = components.get(item, {}).get("minecraft:item_name", {})
        key = name.get("translate") if isinstance(name, dict) else None
        if not key:
            key = f"item.minecraft.{item}"
            print(f"  Warnung: kein item_name für {item}, nutze {key}")
        entries.append((item, key))

    # --- pool.mcfunction schreiben ---------------------------------------
    lines = [
        "# =====================================================================",
        "#  AUTOMATISCH ERZEUGT von generator/generate_items.py – nicht von Hand",
        "#  bearbeiten! Items ausschließen: generator/exclusions.txt",
        f"#  Minecraft {version} – {len(entries)} Items im Pool",
        "# =====================================================================",
        "",
        "# Pool leeren und alle Items einzeln anhängen",
        "data modify storage allitems:game remaining set value []",
    ]
    for item, key in entries:
        lines.append(
            f'data modify storage allitems:game remaining append value {{id:"minecraft:{item}",name:"{key}"}}'
        )
    lines += [
        "",
        "# Gesamtzahl merken (für die Fortschrittsanzeige)",
        "execute store result storage allitems:game total int 1 run data get storage allitems:game remaining",
        "",
    ]
    POOL_FILE.parent.mkdir(parents=True, exist_ok=True)
    POOL_FILE.write_text("\n".join(lines), encoding="utf-8")

    # --- Lesbare Liste ----------------------------------------------------
    list_lines = [f"# Item-Pool für Minecraft {version} ({len(entries)} Items)", ""]
    list_lines += [f"{item}\t{lang_de.get(key, '?')}" for item, key in entries]
    ITEM_LIST_FILE.write_text("\n".join(list_lines) + "\n", encoding="utf-8")

    # --- pack.mcmeta ------------------------------------------------------
    # Gleiches Format wie die pack.mcmeta des Vanilla-Spiels: min_format/max_format
    # als [Haupt, Neben]; pack_format bleibt für ältere Tools zusätzlich drin.
    major, minor = pack_format
    mcmeta = {
        "pack": {
            "description": PACK_DESCRIPTION,
            "pack_format": major,
            "min_format": [major, minor],
            "max_format": [major, minor],
        }
    }
    PACK_MCMETA.write_text(json.dumps(mcmeta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    excluded = len(registry) - len(entries)
    print(f"Fertig: {len(entries)} Items im Pool, {excluded} ausgeschlossen, pack_format {major}.{minor}.")


if __name__ == "__main__":
    main()
