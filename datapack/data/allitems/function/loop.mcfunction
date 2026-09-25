# =====================================================================
#  All Items – loop
#  Plant sich selbst alle 10 Ticks neu ein, bearbeitet die Trigger und
#  prüft, ob ein Spieler das aktuelle Ziel-Item hat.
# =====================================================================

schedule function allitems:loop 10t replace

# Alle Spieler sehen die Bossbar (auch neu beigetretene)
bossbar set allitems:target players @a

# Begrüßung für neue und zurückkehrende Spieler (zeigt das aktuelle Ziel)
execute as @a[tag=!allitems.seen] run function allitems:internal/welcome
execute as @a[scores={allitems.left=1..}] run function allitems:internal/welcome

# Trigger freischalten und auswerten (limit=1: bei gleichzeitigem Skip
# von zwei Spielern wird trotzdem nur EIN Item übersprungen)
scoreboard players enable @a allitems.skip
scoreboard players enable @a allitems.status
execute as @a[scores={allitems.status=1..}] run function allitems:internal/trigger_status
execute as @a[scores={allitems.skip=1}] run function allitems:internal/skip_confirm
execute as @a[scores={allitems.skip=2..},limit=1] run function allitems:internal/trigger_skip

# Nur prüfen, wenn ein Spiel läuft und es ein Ziel gibt
execute unless data storage allitems:game {running:1b} run return 0
execute unless data storage allitems:game target run return 0

# Gemeinsames Ziel: es reicht, wenn EIN Spieler das Item hat
function allitems:internal/check with storage allitems:game target
