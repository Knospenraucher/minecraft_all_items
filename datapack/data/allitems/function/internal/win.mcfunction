# =====================================================================
#  internal/win – alle Items gesammelt, Spiel beendet
# =====================================================================

data modify storage allitems:game running set value 0b
data modify storage allitems:game finished set value 1b
data remove storage allitems:game target

# Bossbar voll und grün
function allitems:internal/count
bossbar set allitems:target color green
execute store result bossbar allitems:target value run bossbar get allitems:target max
bossbar set allitems:target name {"text":"★ Alle Items gesammelt! ★","color":"green","bold":true}

# Titel, Sound und Chatnachricht
title @a times 10 100 20
# Untertitel zuerst setzen – er erscheint erst mit dem nächsten title-Befehl
title @a subtitle {"text":"Ihr habt alle Items gesammelt!","color":"yellow"}
title @a title {"text":"★ GESCHAFFT! ★","color":"gold","bold":true}
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
execute as @a at @s run playsound minecraft:entity.firework_rocket.twinkle master @s ~ ~ ~ 1 1
tellraw @a {"text":"==============================","color":"gold"}
tellraw @a {"text":"  ★ ALL ITEMS – GESCHAFFT! ★","color":"gold","bold":true}
tellraw @a ["",{"text":"  Gesammelt: ","color":"gray"},{"score":{"name":"#collected","objective":"allitems"},"color":"green"},{"text":"  Übersprungen: ","color":"gray"},{"score":{"name":"#skipped","objective":"allitems"},"color":"red"}]
tellraw @a {"text":"==============================","color":"gold"}
