# All Items – Minecraft-Datapack

Ein Datapack für **Minecraft Java Edition 26.3**, mit dem ihr gemeinsam versucht, **jedes Item im Spiel** zu sammeln.

## Spielidee

- Die Challenge **startet automatisch**, sobald das Datapack in der Welt geladen ist. Ihr bekommt direkt ein zufälliges Ziel-Item.
- Sobald **einer von euch** das Item im Inventar hat, gilt es für alle als gesammelt. Dann gibt es sofort das nächste zufällige Ziel, ebenfalls für alle gleich.
- Kein Item kommt doppelt vor. Das Spiel endet, wenn alle Items gesammelt sind.
- Die Bossbar oben zeigt das aktuelle Ziel und den Fortschritt, z. B. **„Item 43/1534: Diamant“**. Beim Betreten der Welt steht das aktuelle Ziel außerdem im Chat.
- Bei jedem Fund gibt es einen Titel, einen Sound und eine Chatnachricht mit dem Namen des Finders.

Der Fortschritt steht in der Command Storage der Welt (`allitems:game`). Nach einem Neustart des Servers oder der Welt geht also nichts verloren.

## Installation

1. Ladet `dist/All_Items.zip` herunter.
2. **Neue Welt:** Beim Erstellen der Welt auf **„Datenpakete“** klicken und die ZIP-Datei in das Fenster ziehen.
   **Bestehende Welt:** Die ZIP-Datei in den Ordner `.minecraft/saves/<Weltname>/datapacks/` kopieren (auf einem Server: `<Weltordner>/datapacks/`).
3. Die Welt öffnen bzw. auf einem laufenden Server `/reload` eingeben.
4. Die Challenge startet sofort: Oben erscheint die Bossbar mit dem ersten Ziel. Mit `/datapack list` seht ihr, ob `file/All_Items.zip` aktiv ist.

## Befehle

Diese Befehle funktionieren für alle Spieler, **auch ohne Cheats**:

| Befehl | Wirkung |
|---|---|
| `/trigger allitems.skip` | Überspringt das aktuelle Item, z. B. wenn es nicht erhältlich ist. Im Chat kommt eine Rückfrage, erst ein Klick auf **[Ja]** überspringt wirklich. Das Item kommt nicht wieder und das Gesamtziel sinkt um 1. |
| `/trigger allitems.status` | Zeigt das aktuelle Ziel und die Zahl der gesammelten, übersprungenen und offenen Items. |

Nur für OPs bzw. mit aktivierten Cheats:

| Befehl | Wirkung |
|---|---|
| `/function allitems:reset` | Löscht den gesamten Fortschritt und startet sofort eine neue Runde. |
| `/function allitems:skip` | Überspringt ohne Rückfrage. |
| `/function allitems:status` | Wie `/trigger allitems.status`. |

## Regeln im Detail

- **Wo muss das Item sein?** Irgendwo im Inventar (inkl. Hotbar), in der Offhand, in einem Rüstungsslot oder am Mauszeiger.
- **Wie oft wird geprüft?** Alle 10 Ticks (zweimal pro Sekunde), nicht in jedem Tick.
- **Wer zählt?** Nur Spieler im Überlebens- oder Abenteuermodus. Kreativ und Zuschauer zählen nicht, damit man nicht aus Versehen schummelt.
- **Das Item wird nicht weggenommen.** Ihr dürft es behalten und weiterverwenden.
- **Überspringen:** Übersprungene Items zählen nicht als gesammelt. Aus `Item 43/1534` wird beim Überspringen `Item 43/1533`.
- **Tränke, verzauberte Bücher usw.:** Jede Item-Art kommt einmal vor. Für „Trank“ reicht also irgendein Trank, für „Verzaubertes Buch“ irgendein verzaubertes Buch.

## Item-Liste und Ausschlüsse

Die Item-Liste wird **nicht von Hand gepflegt**, sondern per Python-Skript aus den offiziellen Spieldaten erzeugt. Für 26.3 sind es **1534 Items** (von 1658 insgesamt). Die komplette Liste mit deutschen Namen steht in [`generator/item_list.txt`](generator/item_list.txt).

Ausgeschlossen sind alle Items, die man im Survival nicht bekommen kann: Bedrock, Befehlsblöcke, Barriere, Konstruktionsblöcke, Verbundblock, Lichtblock, Debug-Stab, Spawn-Eier, Buch des Wissens, versteinerte Eichenholzstufe, Amethystknospenblock, verstärkter Tiefenschiefer, Spielerkopf und einige weitere. Die Ausschlussliste liegt in [`generator/exclusions.txt`](generator/exclusions.txt), mit einem Eintrag pro Zeile und Platzhaltern wie `*_spawn_egg`.

Drin bleiben schwierige, aber mögliche Items wie Drachenei, Mob-Köpfe, Verzauberter goldener Apfel oder Schwerer Kern. Wer sie nicht will, trägt sie in `exclusions.txt` ein.

### Liste neu erzeugen (z. B. bei einer neuen Minecraft-Version)

Ihr braucht Python 3 und eine Internetverbindung. Zusätzliche Pakete sind nicht nötig.

```bash
python3 generator/generate_items.py --version 26.3      # Item-Pool + pack.mcmeta neu erzeugen
python3 tools/build.py                                  # prüfen und dist/All_Items.zip bauen
```

Das Skript lädt die Item-Registry, die Übersetzungsschlüssel und den passenden `pack_format` der angegebenen Version aus [misode/mcmeta](https://github.com/misode/mcmeta). Die Daten dort stammen direkt aus dem Vanilla-Spiel. Danach wendet es die Ausschlussliste an und schreibt:

- `datapack/data/allitems/function/internal/pool.mcfunction` (der Item-Pool)
- `datapack/pack.mcmeta` (mit korrektem `pack_format`)
- `generator/item_list.txt` (lesbare Liste)

Neue Items einer neuen Version kommen so automatisch dazu. Hat sich an den Befehlen selbst etwas geändert, meldet das die Prüfung in `tools/validate.py`.

## Prüfung ohne Minecraft

`python3 tools/validate.py` prüft das Datapack gegen die echten Spieldaten von 26.3:

- alle JSON-Dateien und `pack.mcmeta` auf Gültigkeit, inklusive des richtigen `pack_format` (121)
- jede Befehlszeile gegen den offiziellen Befehlsbaum des Spiels
- Text-Komponenten (Felder, Farben, Übersetzungsschlüssel, neues `click_event`/`hover_event`-Format)
- Item-IDs, Sound-Namen, Inventar-Slots und aufgerufene Funktionen
- Macro-Zeilen (`$…`) mit Beispielwerten für die Variablen

Das ersetzt keinen Test im Spiel, fängt aber Tipp- und Syntaxfehler ab.

## Aufbau

```
datapack/                      Inhalt der ZIP-Datei
├── pack.mcmeta                pack_format 121 (Minecraft 26.3)
└── data/
    ├── minecraft/tags/function/load.json   ruft allitems:load beim Laden auf
    └── allitems/function/
        ├── reset / skip / status           Befehle (skip/status auch per /trigger)
        ├── load                            Scoreboard, Bossbar, Schleife, Autostart
        ├── loop                            alle 10 Ticks: Ziel-Item prüfen
        └── internal/                       interne Hilfsfunktionen
            ├── pool                        (generiert) füllt den Item-Pool
            ├── new_game                    neue Runde aufsetzen (Autostart/reset)
            ├── welcome, help               Begrüßung beim Betreten, klickbare Befehle
            ├── trigger_*, skip_*           /trigger-Befehle mit Rückfrage beim Skip
            ├── next, roll, pick            Zufallsauswahl mit /random + Macros
            ├── check, collect              Erkennung per "execute if items"
            ├── bossbar, bossbar_name       Anzeige
            ├── announce_*, status_target   Chat, Titel, Sounds
            ├── count                       Zahlen für Anzeige/Status
            └── win                         Siegesnachricht
generator/
├── generate_items.py          erzeugt den Item-Pool
├── exclusions.txt             Ausschlussliste (frei bearbeitbar)
└── item_list.txt              (generiert) alle Items mit deutschem Namen
tools/
├── validate.py                Prüfung ohne Minecraft
└── build.py                   Prüfung + ZIP bauen
dist/All_Items.zip             fertiges Datapack
```

### Command Storage `allitems:game`

| Feld | Inhalt |
|---|---|
| `running` | `1b`, solange ein Spiel läuft |
| `finished` | `1b`, wenn alle Items gesammelt sind |
| `total` | Anzahl der Items im Pool beim Start |
| `remaining` | noch nicht gezogene Items `[{id:"minecraft:…",name:"item.minecraft.…"}, …]` |
| `target` | aktuelles Ziel-Item |
| `collected` | gesammelte Items |
| `skipped` | übersprungene Items |

Mit `/data get storage allitems:game collected` könnt ihr euch z. B. alle bisher gesammelten Items anzeigen lassen.

## Deinstallieren

Die ZIP-Datei aus dem `datapacks`-Ordner löschen und `/reload` eingeben. Danach `/bossbar remove allitems:target` und `/scoreboard objectives remove allitems` sowie `allitems.skip`, `allitems.status` und `allitems.left` entfernen. Fertig.
