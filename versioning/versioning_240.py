"""Handle changes between 2.4.0 and 2.5.0."""

from bpy.types import (
    BlendData,
    Object,
)


def update_lods(obj: Object):
    lods_props = obj.get("sollumz_lods", None)
    if lods_props is None:
        return

    lods_arr = lods_props.get("lods", None)
    if lods_arr is None or len(lods_arr) == 0:
        return

    # Get LODs from the old property group
    active_lod_index = lods_props.get("active_lod_index", -1)
    active_lod_level_int = None

    new_lods = {}
    for i, lod_props in enumerate(lods_arr):
        lod_level_int = lod_props.get("level", -1)
        if not 0 <= lod_level_int <= 4:
            continue

        mesh = lod_props.get("mesh", None)
        if mesh is None:
            continue

        new_lods[lod_level_int] = mesh
        if i == active_lod_index:
            active_lod_level_int = lod_level_int

    # Delete the old LOD properties
    del obj["sollumz_lods"]

    # Create the new LOD properties
    obj["sz_lods"] = {}
    new_lods_props = obj["sz_lods"]
    if active_lod_level_int is not None:
        new_lods_props["active_lod_level"] = active_lod_level_int
        new_lods_props["active_lod_level_prev"] = active_lod_level_int

    lod_prop_names = [
        # field names in class LODLevels(PropertyGroup)
        "high",       # 0
        "medium",     # 1
        "low",        # 2
        "very_low",   # 3
        "very_high",  # 4
    ]
    for new_lod_level, new_lod_mesh in new_lods.items():
        lod_prop_name = lod_prop_names[new_lod_level]
        new_lods_props[lod_prop_name] = {}
        new_lod_props = new_lods_props[lod_prop_name]
        new_lod_props["has_mesh"] = new_lod_mesh is not None
        if new_lod_level != active_lod_level_int:
            # only non-active LODs keep a reference to the mesh
            new_lod_props["mesh_ref"] = new_lod_mesh


def do_versions(data_version: int, data: BlendData):
    if data_version < 2:
        for obj in data.objects:
            update_lods(obj)