# =====================================================================
#  internal/announce_skip (Macro) – $(id), $(name) des Ziel-Items
# =====================================================================

$tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"translate":"$(name)","color":"red","hover_event":{"action":"show_item","id":"$(id)"}},{"text":" wurde übersprungen.","color":"gray"}]
execute as @a at @s run playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.7
