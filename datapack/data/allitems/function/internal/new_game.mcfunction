# =====================================================================
#  internal/new_game – setzt eine neue Runde auf und zieht das erste Ziel
#  Wird automatisch beim ersten Laden der Welt und nach reset ausgeführt.
# =====================================================================

# Listen leeren, Item-Pool füllen
data modify storage allitems:game collected set value []
data modify storage allitems:game skipped set value []
data remove storage allitems:game finished
function allitems:internal/pool
data modify storage allitems:game running set value 1b

# Bossbar für alle einblenden
bossbar set allitems:target color yellow
bossbar set allitems:target players @a
bossbar set allitems:target visible true

tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Los geht's! Sammelt gemeinsam alle ","color":"green"},{"nbt":"total","storage":"allitems:game","color":"yellow"},{"text":" Items.","color":"green"}]
execute as @a at @s run playsound minecraft:event.raid.horn master @s ~ ~ ~ 0.6 1.2

# Erstes Ziel ziehen
function allitems:internal/next
