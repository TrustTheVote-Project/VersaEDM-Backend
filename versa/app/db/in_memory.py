from typing import Any, Dict, List, Tuple
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

    def get(self, obj_id: str, external_id_type: str = None):
        if external_id_type is None:
            return self.by_id.get(obj_id)
        else:
            return self.get(self.by_external_id.get((external_id_type, obj_id)))

    def put(self, value: Any):
        obj_id = getattr(value, 'obj_id', uuid4().hex)
        external_ids = getattr(value, 'external_identifier', [])
        self.by_id[obj_id] = value
        for external_id in external_ids:
            self.by_external_id[(self._external_id_type_key(external_id), external_id.value)] = obj_id

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
