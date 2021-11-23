from typing import Literal, Optional, List

from pydantic import BaseModel, Field

from .external_identifier import ExternalIdentifier
from .intl_text import InternationalizedText
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectId, ObjectIdRef


class Person(BaseModel):
    obj_type: Literal[TypeTags.PersonTag] = Field(TypeTags.PersonTag)
    obj_id: ObjectId

    external_identifier: List[ExternalIdentifier] = []
    first_name: Optional[str]
    full_name: Optional[InternationalizedText]
    last_name: Optional[str]
    middle_name: Optional[str]
    nickname: Optional[str]
    party_id: Optional[ObjectIdRef]
    profession: Optional[InternationalizedText]

    class Config:
        alias_generator = fieldname_alias
