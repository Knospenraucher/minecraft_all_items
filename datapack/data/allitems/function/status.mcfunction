# =====================================================================
#  All Items – status
#  Zeigt den aktuellen Spielstand im Chat.
#  Aufruf: /function allitems:status
# =====================================================================

execute unless data storage allitems:game total run return run tellraw @s ["",{"text":"[All Items] ","color":"gold"},{"text":"Es gibt noch kein Spiel. Neu starten mit ","color":"gray"},{"text":"/function allitems:reset","color":"yellow","click_event":{"action":"suggest_command","command":"/function allitems:reset"}}]

# Zahlen ermitteln (landen im Scoreboard "allitems")
function allitems:internal/count

tellraw @s {"text":"===== All Items – Status =====","color":"gold"}
execute if data storage allitems:game target run function allitems:internal/status_target with storage allitems:game target
execute if data storage allitems:game {finished:1b} run tellraw @s {"text":"Alle Items gesammelt! ★","color":"green","bold":true}
tellraw @s ["",{"text":"Gesammelt: ","color":"gray"},{"score":{"name":"#collected","objective":"allitems"},"color":"green"},{"text":" / ","color":"gray"},{"score":{"name":"#goal","objective":"allitems"},"color":"green"}]
tellraw @s ["",{"text":"Übersprungen: ","color":"gray"},{"score":{"name":"#skipped","objective":"allitems"},"color":"red"}]
tellraw @s ["",{"text":"Noch offen: ","color":"gray"},{"score":{"name":"#open","objective":"allitems"},"color":"yellow"},{"text":" (Pool gesamt: ","color":"dark_gray"},{"score":{"name":"#total","objective":"allitems"},"color":"dark_gray"},{"text":")","color":"dark_gray"}]
