# =====================================================================
#  internal/check (Macro) – $(id) = aktuelles Ziel-Item
#  Prüft Inventar, Offhand, Rüstung und das Item am Mauszeiger aller
#  Spieler im Survival/Adventure. Creative und Zuschauer zählen nicht.
#  "return run" sorgt dafür, dass nur der erste Finder zählt.
# =====================================================================

$execute as @a[gamemode=!creative,gamemode=!spectator] if items entity @s container.* $(id) run return run function allitems:internal/collect
$execute as @a[gamemode=!creative,gamemode=!spectator] if items entity @s weapon.offhand $(id) run return run function allitems:internal/collect
$execute as @a[gamemode=!creative,gamemode=!spectator] if items entity @s armor.* $(id) run return run function allitems:internal/collect
$execute as @a[gamemode=!creative,gamemode=!spectator] if items entity @s player.cursor $(id) run return run function allitems:internal/collect
