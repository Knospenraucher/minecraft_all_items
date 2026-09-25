# =====================================================================
#  internal/roll (Macro) – $(max) = höchster gültiger Index
#  Schreibt eine Zufallszahl 0..max nach tmp.index
# =====================================================================

$execute store result storage allitems:game tmp.index int 1 run random value 0..$(max)
