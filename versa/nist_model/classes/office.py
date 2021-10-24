from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectId, ObjectIdRef
from intl_text import InternationalizedText


class Office(BaseModel):
    _type: Literal[TypeTags.OfficeTag] = Field(TypeTags.OfficeTag)
    _id: ObjectId
    election_district_id = Optional[ObjectIdRef]
    is_partisan: bool = True
    name: InternationalizedText
    office_holder_person_ids: List[ObjectIdRef] = []

    class Config:
        alias_generator = fieldname_alias
