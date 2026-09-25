# =====================================================================
#  internal/pick (Macro) – $(index) = gezogener Listenindex
# =====================================================================

$data modify storage allitems:game target set from storage allitems:game remaining[$(index)]
$data remove storage allitems:game remaining[$(index)]
