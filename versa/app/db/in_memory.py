from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from versa.nist_model.enums.nist import ExternalIdentifierType


class EntityStore:
    by_id: Dict[str, Any] = {}
    by_external_id: Dict[Tuple[str, str], str] = {}

    @staticmethod
    def _external_id_type_key(external_id) -> str:
        id_type = external_id.obj_type
        if id_type == ExternalIdentifierType.other:
            return f'{id_type}:{external_id.other_type}'
        else:
            return id_type

    @staticmethod
    def get_obj_id(obj: Any) -> (str, bool):
        obj_id = getattr(obj, 'obj_id', None)
        return str(obj_id) or uuid4().hex, bool(obj_id)

    def get(self, obj_id: str, external_id_type: str = None):
        if external_id_type is None:
            return self.by_id.get(obj_id)
        else:
            return self.get(self.by_external_id.get((external_id_type, obj_id)))

    def put(self, value: Any, overwrite: bool = False) -> Optional[str]:
        obj_id, is_new = self.get_obj_id(value)
        if hasattr(value, 'obj_id') and is_new:
            value.obj_id = obj_id
        external_ids = getattr(value, 'external_identifier', [])

        if obj_id in self.by_id and not overwrite:
            raise ValueError(f"Object with id {obj_id} already exists.")
        self.by_id[obj_id] = value
        for external_id in external_ids:
            self.by_external_id[(self._external_id_type_key(external_id), external_id.value)] = obj_id
        return obj_id if is_new else None

    def delete(self, obj_id: str) -> bool:
        try:
            obj = self.get(obj_id)
            for external_id in getattr(obj, 'external_identifier', []):
                del(self.by_external_id[(self._external_id_type_key(external_id), external_id.value)])
            del(self.by_id[obj_id])
            return True
        except:
            return False

    def values(self) -> List[Any]:
        return list(self.by_id.values())


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
