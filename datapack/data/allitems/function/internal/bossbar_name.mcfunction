# =====================================================================
#  internal/bossbar_name (Macro) – $(name), $(collected), $(goal)
# =====================================================================

$bossbar set allitems:target name ["",{"text":"Sammle: ","color":"gray"},{"translate":"$(name)","color":"yellow","bold":true},{"text":" – $(collected)/$(goal)","color":"gray"}]
