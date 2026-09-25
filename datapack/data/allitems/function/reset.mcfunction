# =====================================================================
#  All Items – reset
#  Löscht den kompletten Fortschritt. Danach mit start neu beginnen.
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

# Bossbar ausblenden und zurücksetzen
bossbar set allitems:target visible false
bossbar set allitems:target name ""
bossbar set allitems:target value 0

tellraw @a ["",{"text":"[All Items] ","color":"gold"},{"text":"Fortschritt zurückgesetzt. Neue Runde mit ","color":"gray"},{"text":"/function allitems:start","color":"yellow","click_event":{"action":"suggest_command","command":"/function allitems:start"}}]
