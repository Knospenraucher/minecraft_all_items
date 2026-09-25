# =====================================================================
#  All Items – start
#  Startet eine neue Runde. Aufruf: /function allitems:start
# =====================================================================

# Läuft schon ein Spiel? Dann nur Hinweis ausgeben.
execute if data storage allitems:game {running:1b} run return run tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Das Spiel läuft bereits. ","color":"gray"},{"text":"/function allitems:status","color":"yellow","click_event":{"action":"run_command","command":"/function allitems:status"}}]

# Schon alles gesammelt? Dann muss erst zurückgesetzt werden.
execute if data storage allitems:game {finished:1b} run return run tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Alle Items sind schon gesammelt. Für eine neue Runde: ","color":"gray"},{"text":"/function allitems:reset","color":"yellow","click_event":{"action":"suggest_command","command":"/function allitems:reset"}}]

# Neues Spiel aufsetzen: Listen leeren, Item-Pool füllen
data modify storage allitems:game collected set value []
data modify storage allitems:game skipped set value []
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
