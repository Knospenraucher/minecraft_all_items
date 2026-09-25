#!/usr/bin/env python3
"""
All Items – baut die ZIP-Datei des Datapacks.

Ablauf:  1. Datapack prüfen (tools/validate.py)
         2. Inhalt von datapack/ nach dist/All_Items.zip packen
            (pack.mcmeta liegt dabei direkt in der ZIP-Wurzel)

Aufruf:  python3 tools/build.py [--skip-validate]
"""

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATAPACK = ROOT / "datapack"
OUT = ROOT / "dist" / "All_Items.zip"


def main() -> int:
    if "--skip-validate" not in sys.argv:
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py")])
        if result.returncode != 0:
            print("Abbruch: Prüfung fehlgeschlagen, keine ZIP erstellt.")
            return 1

    OUT.parent.mkdir(exist_ok=True)
    files = sorted(p for p in DATAPACK.rglob("*") if p.is_file())
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            # Feste Reihenfolge und Zeitstempel -> reproduzierbare ZIP
            info = zipfile.ZipInfo(f.relative_to(DATAPACK).as_posix(), date_time=(2025, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, f.read_bytes())
    print(f"Erstellt: {OUT.relative_to(ROOT)} ({len(files)} Dateien, {OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
