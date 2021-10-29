from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .external_identifier import ExternalIdentifier
from .intl_text import InternationalizedText
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectId, ObjectIdRef


class Party(BaseModel):
    obj_type: Literal[TypeTags.PartyTag] = Field(TypeTags.PartyTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    external_identifier: List[ExternalIdentifier] = []
    is_recognized_party: bool = False
    leader_person_ids: List[ObjectIdRef] = []
    name: InternationalizedText

    class Config:
        alias_generator = fieldname_alias
