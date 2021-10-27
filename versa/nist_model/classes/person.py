from typing import Literal, Optional

from pydantic import BaseModel, Field

from intl_text import InternationalizedText
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectId, ObjectIdRef


class Person(BaseModel):
    _type: Literal[TypeTags.PersonTag] = Field(TypeTags.PersonTag)
    _id: ObjectId
    first_name: Optional[str]
    full_name: InternationalizedText
    last_name: Optional[str]
    middle_name: Optional[str]
    nickname: Optional[str]
    party_id: Optional[ObjectIdRef]
    profession: Optional[InternationalizedText]

    class Config:
        alias_generator = fieldname_alias
