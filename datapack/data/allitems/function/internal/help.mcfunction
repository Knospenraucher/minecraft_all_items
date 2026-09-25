# =====================================================================
#  internal/help – zeigt die Befehle (klickbar) für @s
# =====================================================================

tellraw @s ["",{"text":"Befehle: ","color":"gray"},{"text":"[Überspringen]","color":"red","click_event":{"action":"suggest_command","command":"/trigger allitems.skip"},"hover_event":{"action":"show_text","value":"/trigger allitems.skip"}},{"text":" "},{"text":"[Status]","color":"aqua","click_event":{"action":"run_command","command":"/trigger allitems.status"},"hover_event":{"action":"show_text","value":"/trigger allitems.status"}}]
