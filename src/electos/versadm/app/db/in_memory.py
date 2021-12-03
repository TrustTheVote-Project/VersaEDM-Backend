from typing import Any, Dict, List, Optional
from uuid import uuid4


class EntityStore:
    def __init__(self):
        self.id_to_obj: Dict[str, Any] = {}
        self.id_synonyms: Dict[str, str] = {}

    @staticmethod
    def get_obj_id(obj: Any) -> (str, bool):
        obj_id = getattr(obj, 'obj_id', None)
        return str(obj_id) if obj_id else uuid4().hex, not bool(obj_id)

    def by_ref(self, obj_id: str):
        return self.id_to_obj[obj_id]

    def get(self, obj_or_external_id: str):
        return self.id_to_obj.get(self.id_synonyms.get(obj_or_external_id))

    def put(self, value: Any, overwrite: bool = False) -> Optional[str]:
        obj_id, is_generated_id = self.get_obj_id(value)
        # if we had to generate an id, see if the external identifiers resolve to a single known id
        external_ids = {ext_id.value for ext_id in getattr(value, 'external_identifier', [])}
        synonym_referents = {self.id_synonyms[ext_id] for ext_id in external_ids if ext_id in self.id_synonyms}
        if is_generated_id:
            if len(synonym_referents) > 1:
                raise ValueError('External ids reference multiple known objects.')
            elif len(synonym_referents) == 1:
                obj_id = list(synonym_referents)[0]
                is_generated_id = False
            elif hasattr(value, 'obj_id'):
                # the external identifiers don't resolve to a known internal id, so use the generated one
                value.obj_id = obj_id
        else:
            if synonym_referents.difference({obj_id}):
                # the external ids refer to different internal ids than this object has
                raise ValueError('External ids reference a different existing object.')

        if not overwrite and obj_id in self.id_to_obj:
            raise ValueError('Object already exists.')

        self.id_to_obj[obj_id] = value
        self.id_synonyms[obj_id] = obj_id
        for external_id in external_ids:
            self.id_synonyms[external_id] = obj_id
        return obj_id if is_generated_id else None

    def delete(self, obj_id: str) -> bool:
        try:
            obj = self.get(obj_id)
            for external_id in getattr(obj, 'external_identifier', []):
                del(self.id_synonyms[external_id.value])
            del(self.id_to_obj[obj_id])
            return True
        except:
            return False

    def values(self) -> List[Any]:
        return list(self.id_to_obj.values())


class InMemoryDb:
    election_report = None
    ballot_styles = EntityStore()
    candidates = EntityStore()
    contests = EntityStore()
    elections = EntityStore()
    offices = EntityStore()
    parties = EntityStore()
    persons = EntityStore()
    reporting_units = EntityStore()
    audit_trail: []

    def hash_state(self) -> str:
        # TODO: actually compute a consistent hash
        return ''
