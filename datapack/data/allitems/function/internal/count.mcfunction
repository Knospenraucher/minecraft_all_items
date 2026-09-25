# =====================================================================
#  internal/count – berechnet die Spielstand-Zahlen im Scoreboard:
#    #total     Items im Pool beim Start
#    #collected gesammelte Items
#    #skipped   übersprungene Items
#    #goal      Gesamtziel = total - skipped
#    #open      noch offene Items (inkl. aktuellem Ziel)
# =====================================================================

execute store result score #total allitems run data get storage allitems:game total
execute store result score #collected allitems run data get storage allitems:game collected
execute store result score #skipped allitems run data get storage allitems:game skipped
scoreboard players operation #goal allitems = #total allitems
scoreboard players operation #goal allitems -= #skipped allitems
execute store result score #open allitems run data get storage allitems:game remaining
execute if data storage allitems:game target run scoreboard players add #open allitems 1
