# =====================================================================
#  internal/announce_target (Macro) – $(id), $(name) des neuen Ziels
# =====================================================================

$tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Neues Ziel: ","color":"gray"},{"translate":"$(name)","color":"yellow","bold":true,"hover_event":{"action":"show_item","id":"$(id)"}}]
execute as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 0.7 1.5
