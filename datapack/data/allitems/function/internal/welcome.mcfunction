# =====================================================================
#  internal/welcome – Begrüßung beim (erneuten) Betreten der Welt
#  @s = beigetretener Spieler
# =====================================================================

tag @s add allitems.seen
scoreboard players reset @s allitems.left

tellraw @s ["",{"text":"[All Items] ","color":"gold"},{"text":"Willkommen zur All-Items-Challenge!","color":"green"}]
execute if data storage allitems:game target run function allitems:internal/status_target with storage allitems:game target
execute if data storage allitems:game {finished:1b} run tellraw @s {"text":"Alle Items sind bereits gesammelt! ★","color":"green"}
function allitems:internal/help
