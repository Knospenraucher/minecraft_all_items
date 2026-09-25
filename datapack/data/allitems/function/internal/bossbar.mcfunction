# =====================================================================
#  internal/bossbar – aktualisiert Text und Füllstand der Bossbar
#  Anzeige: "Item <Nummer>/<Gesamtziel>: <Item>"
# =====================================================================

function allitems:internal/count

# Füllstand (max muss mindestens 1 sein)
execute if score #goal allitems matches ..0 run scoreboard players set #goal allitems 1
execute store result bossbar allitems:target max run scoreboard players get #goal allitems
execute store result bossbar allitems:target value run scoreboard players get #collected allitems

# Werte für das Macro zusammenstellen
# Nummer des aktuellen Items = gesammelt + 1
scoreboard players operation #current allitems = #collected allitems
scoreboard players add #current allitems 1
execute store result storage allitems:game tmp.current int 1 run scoreboard players get #current allitems
execute store result storage allitems:game tmp.goal int 1 run scoreboard players get #goal allitems
data modify storage allitems:game tmp.name set from storage allitems:game target.name
execute if data storage allitems:game target run function allitems:internal/bossbar_name with storage allitems:game tmp

bossbar set allitems:target players @a
bossbar set allitems:target visible true
