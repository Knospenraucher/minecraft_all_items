# =====================================================================
#  internal/announce_collect (Macro) – $(id), $(name) des Ziel-Items
#  @s = Spieler, der das Item gefunden hat
# =====================================================================

title @a times 5 30 10
# Untertitel zuerst setzen – er erscheint erst mit dem nächsten title-Befehl
$title @a subtitle {"translate":"$(name)","color":"aqua"}
title @a title {"text":"✔ Gesammelt!","color":"green","bold":true}
$tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"selector":"@s","color":"yellow"},{"text":" hat ","color":"gray"},{"translate":"$(name)","color":"aqua","hover_event":{"action":"show_item","id":"$(id)"}},{"text":" gesammelt!","color":"gray"}]
