# =====================================================================
#  All Items – skip
#  Überspringt das aktuelle Ziel-Item. Es wird als "übersprungen"
#  gezählt, kommt nicht wieder und verringert das Gesamtziel um 1.
#  Aufruf: /function allitems:skip
# =====================================================================

execute unless data storage allitems:game {running:1b} run return run tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Es läuft gerade kein Spiel.","color":"red"}]

# Meldung ausgeben, Item in die Skip-Liste verschieben, neues Ziel ziehen
function allitems:internal/announce_skip with storage allitems:game target
data modify storage allitems:game skipped append from storage allitems:game target
function allitems:internal/next
