# =====================================================================
#  All Items – loop
#  Plant sich selbst alle 10 Ticks neu ein und prüft, ob ein Spieler
#  das aktuelle Ziel-Item hat.
# =====================================================================

schedule function allitems:loop 10t replace

# Nur prüfen, wenn ein Spiel läuft und es ein Ziel gibt
execute unless data storage allitems:game {running:1b} run return 0
execute unless data storage allitems:game target run return 0

# Neu beigetretene Spieler sehen die Bossbar ebenfalls
bossbar set allitems:target players @a

# Gemeinsames Ziel: es reicht, wenn EIN Spieler das Item hat
function allitems:internal/check with storage allitems:game target
