# =====================================================================
#  All Items – reset (nur für OPs / mit Cheats)
#  Löscht den kompletten Fortschritt und startet sofort eine neue Runde.
#  Aufruf: /function allitems:reset
# =====================================================================

data remove storage allitems:game running
data remove storage allitems:game finished
data remove storage allitems:game total
data remove storage allitems:game remaining
data remove storage allitems:game target
data remove storage allitems:game collected
data remove storage allitems:game skipped
data remove storage allitems:game tmp

tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Fortschritt zurückgesetzt – neue Runde!","color":"gray"}]

function allitems:internal/new_game
