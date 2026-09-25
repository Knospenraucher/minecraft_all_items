# =====================================================================
#  All Items – status
#  Zeigt den aktuellen Spielstand im Chat.
#  Aufruf: /function allitems:status
# =====================================================================

execute unless data storage allitems:game total run return run tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Es gibt noch kein Spiel. Starten mit ","color":"gray"},{"text":"/function allitems:start","color":"yellow","click_event":{"action":"suggest_command","command":"/function allitems:start"}}]

# Zahlen ermitteln (landen im Scoreboard "allitems")
function allitems:internal/count

tellraw @a {"text":"===== All Items – Status =====","color":"gold"}
execute if data storage allitems:game target run function allitems:internal/status_target with storage allitems:game target
execute if data storage allitems:game {finished:1b} run tellraw @a {"text":"Alle Items gesammelt! ★","color":"green","bold":true}
tellraw @a ["",{"text":"Gesammelt: ","color":"gray"},{"score":{"name":"#collected","objective":"allitems"},"color":"green"},{"text":" / ","color":"gray"},{"score":{"name":"#goal","objective":"allitems"},"color":"green"}]
tellraw @a ["",{"text":"Übersprungen: ","color":"gray"},{"score":{"name":"#skipped","objective":"allitems"},"color":"red"}]
tellraw @a ["",{"text":"Noch offen: ","color":"gray"},{"score":{"name":"#open","objective":"allitems"},"color":"yellow"},{"text":" (Pool gesamt: ","color":"dark_gray"},{"score":{"name":"#total","objective":"allitems"},"color":"dark_gray"},{"text":")","color":"dark_gray"}]
