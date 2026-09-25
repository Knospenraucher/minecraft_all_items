# =====================================================================
#  internal/next – zieht das nächste zufällige Ziel-Item
#  Das Item wird aus "remaining" entfernt, kann also nie doppelt kommen.
# =====================================================================

data remove storage allitems:game target

# Keine Items mehr übrig? -> Sieg!
execute store result score #remaining allitems run data get storage allitems:game remaining
execute if score #remaining allitems matches ..0 run return run function allitems:internal/win

# Höchster Index = Anzahl - 1
scoreboard players remove #remaining allitems 1
execute store result storage allitems:game tmp.max int 1 run scoreboard players get #remaining allitems
data modify storage allitems:game tmp.index set value 0

# /random braucht einen Bereich mit mindestens 2 Werten; bei nur noch
# einem Item bleibt der Index einfach 0
execute if score #remaining allitems matches 1.. run function allitems:internal/roll with storage allitems:game tmp

# Item an diesem Index zum Ziel machen und aus dem Pool entfernen
function allitems:internal/pick with storage allitems:game tmp

function allitems:internal/announce_target with storage allitems:game target
function allitems:internal/bossbar
