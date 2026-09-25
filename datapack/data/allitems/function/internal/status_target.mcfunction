# =====================================================================
#  internal/status_target (Macro) – $(id), $(name) des aktuellen Ziels
# =====================================================================

$tellraw @a ["",{"text":"Aktuelles Ziel: ","color":"gray"},{"translate":"$(name)","color":"yellow","bold":true,"hover_event":{"action":"show_item","id":"$(id)"}},{"text":" ($(id))","color":"dark_gray"}]
