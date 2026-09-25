# =====================================================================
#  internal/bossbar – aktualisiert Text und Füllstand der Bossbar
#  Anzeige: "Sammle: <Item> – <gesammelt>/<Gesamtziel>"
# =====================================================================

function allitems:internal/count

# Füllstand (max muss mindestens 1 sein)
execute if score #goal allitems matches ..0 run scoreboard players set #goal allitems 1
execute store result bossbar allitems:target max run scoreboard players get #goal allitems
execute store result bossbar allitems:target value run scoreboard players get #collected allitems

# Werte für das Macro zusammenstellen
execute store result storage allitems:game tmp.collected int 1 run scoreboard players get #collected allitems
execute store result storage allitems:game tmp.goal int 1 run scoreboard players get #goal allitems
data modify storage allitems:game tmp.name set from storage allitems:game target.name
execute if data storage allitems:game target run function allitems:internal/bossbar_name with storage allitems:game tmp

bossbar set allitems:target players @a
bossbar set allitems:target visible true
