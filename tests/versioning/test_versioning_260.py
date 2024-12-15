from .shared import load_blend_data


def test_versioning_archetype_uuids():
    data = load_blend_data("v260_archetype_uuids.blend")

    UUID_LENGTH = 36
    all_uuids = set()

    def _check_uuid(uuid: str, who):
        assert len(uuid) == UUID_LENGTH, f"UUID of '{who}' is invalid: {uuid}"
        assert uuid not in all_uuids, f"UUID of '{who}' already in use: {uuid}"
        all_uuids.add(arch.uuid)

    for scene in data.scenes:
        for ytyp in scene.ytyps:
            for arch in ytyp.archetypes:
                _check_uuid(arch.uuid, arch)
                for e in arch.entities:
                    _check_uuid(e.uuid, e)
                for s in arch.entity_sets:
                    _check_uuid(s.uuid, s)
                for p in arch.portals:
                    _check_uuid(p.uuid, p)
                for r in arch.rooms:
                    _check_uuid(r.uuid, r)