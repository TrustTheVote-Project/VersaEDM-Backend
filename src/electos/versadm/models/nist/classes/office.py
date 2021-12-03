from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.intl_text import InternationalizedText
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectId, ObjectIdRef


class Office(BaseModel):
    obj_type: Literal[TypeTags.OfficeTag] = Field(TypeTags.OfficeTag)
    obj_id: ObjectId

    election_district_id: Optional[ObjectIdRef]
    external_identifier: List[ExternalIdentifier] = []
    is_partisan: bool = True
    name: InternationalizedText
    office_holder_person_ids: List[ObjectIdRef] = []

    class Config:
        alias_generator = fieldname_alias
