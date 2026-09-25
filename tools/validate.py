#!/usr/bin/env python3
"""
All Items – Prüfskript für das Datapack.

Da Minecraft hier nicht gestartet werden kann, prüft dieses Skript das
Datapack so gut es geht gegen die offiziellen Vanilla-Daten (misode/mcmeta):

  * alle .json-Dateien und pack.mcmeta sind gültiges JSON
  * jede Befehlszeile passt zum echten Befehlsbaum (Brigadier) der Version
  * Macro-Zeilen ($...) enthalten Variablen, normale Zeilen keine
  * Text-Komponenten sind gültiges JSON mit bekannten Feldern und Farben
  * aufgerufene Funktionen existieren, Items/Sounds/Slots sind gültig

Aufruf:  python3 tools/validate.py [--version 1.21.10]
Rückgabe: Exit-Code 0 = alles ok, 1 = Fehler gefunden.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATAPACK = ROOT / "datapack"
MCMETA = "https://raw.githubusercontent.com/misode/mcmeta"

# Beispielwerte, mit denen Macro-Variablen zum Prüfen ersetzt werden
MACRO_SAMPLES = {
    "id": "minecraft:diamond",
    "name": "item.minecraft.diamond",
    "max": "41",
    "index": "7",
    "collected": "3",
    "goal": "1369",
}

TEXT_KEYS = {
    "text", "translate", "with", "fallback", "score", "selector", "separator", "keybind", "nbt",
    "storage", "entity", "block", "interpret", "source", "extra", "type", "color", "shadow_color",
    "font", "bold", "italic", "underlined", "strikethrough", "obfuscated", "insertion",
    "click_event", "hover_event",
}
COLORS = {
    "black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray",
    "dark_gray", "blue", "green", "aqua", "red", "light_purple", "yellow", "white",
}
SELECTOR_ARGS = {
    "x", "y", "z", "distance", "dx", "dy", "dz", "scores", "tag", "team", "limit", "sort", "level",
    "gamemode", "name", "x_rotation", "y_rotation", "type", "nbt", "advancements", "predicate",
}
GAMEMODES = {"survival", "creative", "adventure", "spectator"}
SLOT_RE = re.compile(
    r"^(container\.(\*|\d+)|hotbar\.(\*|\d)|inventory\.(\*|\d+)|enderchest\.(\*|\d+)|"
    r"weapon(\.(\*|mainhand|offhand))?|armor\.(\*|head|chest|legs|feet|body)|"
    r"horse\.(\*|saddle|chest|\d+)|villager\.(\*|\d)|player\.(cursor|crafting\.(\*|\d))|"
    r"contents|saddle)$"
)


class ParseError(Exception):
    pass


def fetch_json(url: str):
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)


# ---------------------------------------------------------------------------
#  Hilfsfunktionen zum Einlesen einzelner Argumente
# ---------------------------------------------------------------------------

def read_word(s: str, i: int) -> tuple[str, int]:
    j = i
    while j < len(s) and s[j] != " ":
        j += 1
    if j == i:
        raise ParseError(f"Argument erwartet an Position {i}")
    return s[i:j], j


def read_balanced(s: str, i: int) -> tuple[str, int]:
    """Liest einen Wert mit Klammern ({...} / [...]) inkl. Strings bis zum Ende."""
    depth, j, quote = 0, i, None
    while j < len(s):
        c = s[j]
        if quote:
            if c == "\\":
                j += 1
            elif c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
            if depth < 0:
                raise ParseError("Klammerfehler")
        elif c == " " and depth == 0:
            break
        j += 1
    if quote or depth:
        raise ParseError("Nicht geschlossene Klammer oder Anführungszeichen")
    return s[i:j], j


def check_text_component(value, ctx: "Context") -> None:
    """Prüft eine (als JSON geschriebene) Text-Komponente rekursiv."""
    if isinstance(value, str):
        return
    if isinstance(value, list):
        if not value:
            raise ParseError("Leere Komponenten-Liste")
        for v in value:
            check_text_component(v, ctx)
        return
    if not isinstance(value, dict):
        raise ParseError(f"Ungültige Text-Komponente: {value!r}")
    unknown = set(value) - TEXT_KEYS
    if unknown:
        raise ParseError(f"Unbekannte Felder in Text-Komponente: {sorted(unknown)}")
    if "color" in value and value["color"] not in COLORS and not re.fullmatch(r"#[0-9A-Fa-f]{6}", value["color"]):
        raise ParseError(f"Unbekannte Farbe: {value['color']}")
    if "translate" in value and value["translate"] not in ctx.lang:
        raise ParseError(f"Unbekannter Übersetzungsschlüssel: {value['translate']}")
    if "score" in value and set(value["score"]) != {"name", "objective"}:
        raise ParseError("score braucht name und objective")
    if "nbt" in value and not {"storage", "entity", "block"} & set(value):
        raise ParseError("nbt-Komponente ohne storage/entity/block")
    if "selector" in value:
        parse_selector(value["selector"], ctx)
    if "click_event" in value:
        ce = value["click_event"]
        if ce.get("action") in ("run_command", "suggest_command") and "command" not in ce:
            raise ParseError("click_event braucht ab 1.21.5 das Feld 'command'")
    if "hover_event" in value:
        he = value["hover_event"]
        if he.get("action") == "show_item" and "id" not in he:
            raise ParseError("hover_event show_item braucht ab 1.21.5 das Feld 'id'")
        if he.get("action") == "show_item":
            ctx.check_item(he["id"])
    for key in ("extra", "with"):
        if key in value:
            for v in value[key]:
                check_text_component(v, ctx)


def parse_selector(tok: str, ctx: "Context") -> None:
    m = re.fullmatch(r"@([parsen])(\[(.*)\])?", tok)
    if not m:
        if tok.startswith("@"):
            raise ParseError(f"Ungültiger Selektor: {tok}")
        return  # Spielername / Fake-Player wie #goal
    if m.group(3):
        for part in m.group(3).split(","):
            key, _, val = part.partition("=")
            if key.strip() not in SELECTOR_ARGS:
                raise ParseError(f"Unbekanntes Selektor-Argument: {key}")
            if key == "gamemode" and val.lstrip("!") not in GAMEMODES:
                raise ParseError(f"Unbekannter Spielmodus: {val}")


# ---------------------------------------------------------------------------
#  Befehlsbaum-Parser
# ---------------------------------------------------------------------------

class Context:
    def __init__(self, tree, items, sounds, lang, functions):
        self.tree = tree
        self.items = items
        self.sounds = sounds
        self.lang = lang
        self.functions = functions

    def check_item(self, item_id: str) -> None:
        if item_id.removeprefix("minecraft:") not in self.items:
            raise ParseError(f"Unbekanntes Item: {item_id}")

    # Liest ein Argument; gibt neue Position zurück oder wirft ParseError
    def read_argument(self, node: dict, cmd: list[str], s: str, i: int) -> int:
        parser = node["parser"]
        props = node.get("properties", {})
        if parser in ("minecraft:component",):
            raw, j = read_balanced(s, i)
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as e:
                raise ParseError(f"Text-Komponente ist kein gültiges JSON/SNBT: {e}")
            check_text_component(value, self)
            return j
        if parser in ("minecraft:nbt_compound_tag", "minecraft:nbt_tag", "minecraft:nbt_path",
                      "minecraft:style"):
            _, j = read_balanced(s, i)
            return j
        if parser in ("minecraft:entity", "minecraft:score_holder", "minecraft:game_profile"):
            tok, j = read_balanced(s, i)
            parse_selector(tok, self)
            if props.get("amount") == "single" and tok.startswith(("@a", "@e")) and "limit=1" not in tok:
                raise ParseError(f"Selektor muss genau ein Ziel haben: {tok}")
            return j
        if parser == "minecraft:item_predicate":
            tok, j = read_balanced(s, i)
            item = tok.split("[", 1)[0]
            if item != "*" and not item.startswith("#"):
                self.check_item(item)
            return j
        if parser == "minecraft:item_slots":
            tok, j = read_word(s, i)
            if not SLOT_RE.match(tok):
                raise ParseError(f"Unbekannter Slot: {tok}")
            return j
        if parser == "minecraft:function":
            tok, j = read_word(s, i)
            name = tok.lstrip("#")
            if tok.startswith("#"):
                pass
            elif name not in self.functions and not name.startswith("minecraft:"):
                raise ParseError(f"Funktion existiert nicht: {tok}")
            return j
        if parser in ("brigadier:integer", "brigadier:float", "brigadier:double"):
            tok, j = read_word(s, i)
            num = int(tok) if parser == "brigadier:integer" else float(tok)
            if "min" in props and num < props["min"] or "max" in props and num > props["max"]:
                raise ParseError(f"Zahl {tok} außerhalb des erlaubten Bereichs")
            return j
        if parser == "brigadier:bool":
            tok, j = read_word(s, i)
            if tok not in ("true", "false"):
                raise ParseError("true/false erwartet")
            return j
        if parser == "minecraft:int_range":
            tok, j = read_word(s, i)
            if not re.fullmatch(r"-?\d+|-?\d*\.\.-?\d*", tok) or tok == "..":
                raise ParseError(f"Ungültiger Bereich: {tok}")
            return j
        if parser == "minecraft:time":
            tok, j = read_word(s, i)
            if not re.fullmatch(r"\d+(\.\d+)?[tsd]?", tok):
                raise ParseError(f"Ungültige Zeit: {tok}")
            return j
        if parser in ("minecraft:vec3", "minecraft:block_pos"):
            j = i
            for n in range(3):
                tok, j = read_word(s, j)
                if not re.fullmatch(r"[~^]?-?\d*\.?\d*", tok):
                    raise ParseError(f"Ungültige Koordinate: {tok}")
                if n < 2:
                    if j >= len(s):
                        raise ParseError("Koordinate fehlt")
                    j += 1
            return j
        if parser == "minecraft:gamemode":
            tok, j = read_word(s, i)
            if tok not in GAMEMODES:
                raise ParseError(f"Unbekannter Spielmodus: {tok}")
            return j
        if parser in ("minecraft:message",) or (parser == "brigadier:string" and props.get("type") == "greedy"):
            return len(s)
        if parser == "minecraft:resource_location" and cmd[:1] == ["playsound"]:
            tok, j = read_word(s, i)
            if tok.removeprefix("minecraft:") not in self.sounds:
                raise ParseError(f"Unbekannter Sound: {tok}")
            return j
        tok, j = read_word(s, i)
        return j

    def parse(self, s: str) -> None:
        if not self._walk(self.tree, s, 0, []):
            raise ParseError(self.last_error or "Befehl passt nicht zum Befehlsbaum")

    def _walk(self, node: dict, s: str, i: int, path: list[str]) -> bool:
        # Ende erreicht?
        if i >= len(s):
            if node.get("executable"):
                return True
            self.last_error = f"Unvollständiger Befehl nach '{' '.join(path)}'"
            return False
        if node is not self.tree:
            if s[i] != " ":
                self.last_error = f"Leerzeichen erwartet an Position {i}"
                return False
            i += 1
        # Umleitungen (z.B. execute ... -> execute, "run" -> Wurzel)
        children = node.get("children")
        if "redirect" in node:
            children = self.tree["children"][node["redirect"][0]]["children"]
        elif children is None and node is not self.tree:
            children = self.tree["children"]
        # Erst Literale, dann Argumente probieren (mit Backtracking)
        for name, child in children.items():
            if child["type"] == "literal":
                if s.startswith(name, i) and (i + len(name) == len(s) or s[i + len(name)] == " "):
                    if self._walk(child, s, i + len(name), path + [name]):
                        return True
        for name, child in children.items():
            if child["type"] == "argument":
                try:
                    j = self.read_argument(child, path, s, i)
                except (ParseError, ValueError) as e:
                    self.last_error = f"'{name}' nach '{' '.join(path)}': {e}"
                    continue
                if self._walk(child, s, j, path + [f"<{name}>"]):
                    return True
        if not getattr(self, "last_error", None):
            self.last_error = f"Unbekanntes Wort nach '{' '.join(path)}'"
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="1.21.10")
    version = parser.parse_args().version

    errors: list[str] = []

    # --- 1. JSON-Dateien ---------------------------------------------------
    json_files = [DATAPACK / "pack.mcmeta", *DATAPACK.rglob("*.json")]
    for f in json_files:
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{f.relative_to(ROOT)}: ungültiges JSON: {e}")
    print(f"JSON: {len(json_files)} Dateien geprüft")

    # --- 2. Vanilla-Daten laden -------------------------------------------
    print(f"Lade Vanilla-Daten für {version} …")
    tree = fetch_json(f"{MCMETA}/{version}-summary/commands/data.json")
    items = set(fetch_json(f"{MCMETA}/{version}-registries/item/data.json"))
    sounds = set(fetch_json(f"{MCMETA}/{version}-registries/sound_event/data.json"))
    lang = fetch_json(f"{MCMETA}/{version}-assets-json/assets/minecraft/lang/en_us.json")

    # pack_format prüfen
    mcmeta = json.loads((DATAPACK / "pack.mcmeta").read_text(encoding="utf-8"))["pack"]
    versions = fetch_json(f"{MCMETA}/refs/heads/summary/versions/data.json")
    expected = next(v["data_pack_version"] for v in versions if v["id"] == version)
    for key in ("pack_format", "min_format", "max_format"):
        if mcmeta.get(key) != expected:
            errors.append(f"pack.mcmeta: {key} ist {mcmeta.get(key)}, erwartet {expected}")

    # Alle vorhandenen Funktionen sammeln
    functions = set()
    for ns_dir in (DATAPACK / "data").iterdir():
        fdir = ns_dir / "function"
        if fdir.is_dir():
            for f in fdir.rglob("*.mcfunction"):
                functions.add(f"{ns_dir.name}:{f.relative_to(fdir).with_suffix('').as_posix()}")
    # Function-Tags prüfen
    for tag in (DATAPACK / "data").glob("*/tags/function/*.json"):
        for v in json.loads(tag.read_text(encoding="utf-8"))["values"]:
            if v not in functions:
                errors.append(f"{tag.relative_to(ROOT)}: Funktion {v} existiert nicht")

    ctx = Context(tree, items, sounds, lang, functions)

    # --- 3. Befehle -------------------------------------------------------
    count = 0
    for f in sorted(DATAPACK.rglob("*.mcfunction")):
        rel = f.relative_to(ROOT)
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            count += 1
            if line.startswith("$"):
                variables = re.findall(r"\$\(([A-Za-z0-9_]+)\)", line)
                if not variables:
                    errors.append(f"{rel}:{n}: Macro-Zeile ohne $(variable)")
                    continue
                missing = [v for v in variables if v not in MACRO_SAMPLES]
                if missing:
                    errors.append(f"{rel}:{n}: keine Beispielwerte für Macro-Variablen {missing}")
                    continue
                line = re.sub(r"\$\(([A-Za-z0-9_]+)\)", lambda m: MACRO_SAMPLES[m.group(1)], line[1:])
            elif "$(" in line:
                errors.append(f"{rel}:{n}: $(…) in einer Zeile ohne führendes $")
                continue
            ctx.last_error = None
            try:
                ctx.parse(line)
            except ParseError as e:
                errors.append(f"{rel}:{n}: {e}\n    {line[:160]}")
    print(f"Befehle: {count} Zeilen in {len(functions)} Funktionen geprüft")

    if errors:
        print(f"\n{len(errors)} Fehler:")
        for e in errors:
            print(" -", e)
        return 1
    print("Alles in Ordnung.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
