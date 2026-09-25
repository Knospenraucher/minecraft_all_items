# =====================================================================
#  internal/skip_question (Macro) – $(id), $(name) des aktuellen Ziels
# =====================================================================

$tellraw @s ["",{"text":"[All Items] ","color":"gold"},{"translate":"$(name)","color":"yellow","hover_event":{"action":"show_item","id":"$(id)"}},{"text":" wirklich überspringen? ","color":"gray"},{"text":"[Ja]","color":"red","bold":true,"click_event":{"action":"run_command","command":"/trigger allitems.skip set 2"},"hover_event":{"action":"show_text","value":"Item überspringen"}}]
