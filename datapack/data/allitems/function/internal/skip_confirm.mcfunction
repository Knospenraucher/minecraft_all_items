# =====================================================================
#  internal/skip_confirm – /trigger allitems.skip (Stufe 1)
#  Fragt nach, damit niemand aus Versehen überspringt. Der Klick auf
#  [Ja] setzt den Trigger auf 2 -> internal/trigger_skip.
# =====================================================================

scoreboard players set @s allitems.skip 0
execute unless data storage allitems:game {running:1b} run return run tellraw @s ["",{"text":"[All Items] ","color":"gold"},{"text":"Es läuft gerade kein Spiel.","color":"red"}]
function allitems:internal/skip_question with storage allitems:game target
