# =====================================================================
#  internal/bossbar_name (Macro) – $(name), $(current), $(goal)
#  Anzeige z.B.: "Item 43/1369: Diamant"
# =====================================================================

$bossbar set allitems:target name ["",{"text":"Item $(current)/$(goal): ","color":"white"},{"translate":"$(name)","color":"yellow","bold":true}]
