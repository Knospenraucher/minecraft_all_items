# =====================================================================
#  All Items – load
#  Wird bei jedem Laden der Welt und bei /reload automatisch ausgeführt
#  (über den Function-Tag #minecraft:load).
#
#  Aufbau der Command Storage "allitems:game":
#    running   1b solange ein Spiel läuft
#    finished  1b wenn alle Items gesammelt wurden
#    total     Anzahl Items im Pool beim Spielstart
#    remaining Liste der noch nicht gezogenen Items  [{id:"...",name:"..."}]
#    target    aktuelles Ziel-Item                    {id:"...",name:"..."}
#    collected Liste der gesammelten Items
#    skipped   Liste der übersprungenen Items
#    tmp       Zwischenwerte für Function-Macros
#  Die Storage wird mit der Welt gespeichert, nach einem Neustart geht
#  also nichts verloren.
# =====================================================================

# Scoreboard nur für Zwischenrechnungen (echter Spielstand liegt in der Storage)
scoreboard objectives add allitems dummy

# Bossbar anlegen (schlägt still fehl, falls sie schon existiert)
bossbar add allitems:target ""
bossbar set allitems:target style progress

# Prüf-Schleife starten: läuft alle 10 Ticks statt jeden Tick
schedule function allitems:loop 10t replace

# Bossbar nach dem Laden wieder auf den aktuellen Stand bringen
execute if data storage allitems:game {running:1b} run function allitems:internal/bossbar

tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Datapack geladen. ","color":"gray"},{"text":"/function allitems:start","color":"yellow","click_event":{"action":"suggest_command","command":"/function allitems:start"}}]
