# =====================================================================
#  internal/collect – Ziel-Item wurde gefunden
#  Ausgeführt als der Spieler (@s), der das Item hat.
# =====================================================================

# Titel und Chatnachricht an alle (mit Name des Finders)
function allitems:internal/announce_collect with storage allitems:game target

# Erfolgs-Sound für alle Spieler
execute as @a at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.2

# Item als gesammelt speichern und nächstes Ziel ziehen
data modify storage allitems:game collected append from storage allitems:game target
function allitems:internal/next
