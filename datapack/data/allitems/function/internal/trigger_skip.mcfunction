# =====================================================================
#  internal/trigger_skip – /trigger allitems.skip set 2 (bestätigt)
#  @s = Spieler, der überspringt
# =====================================================================

# Alle Skip-Trigger zurücksetzen, damit nicht doppelt übersprungen wird
scoreboard players set @a allitems.skip 0
function allitems:skip
