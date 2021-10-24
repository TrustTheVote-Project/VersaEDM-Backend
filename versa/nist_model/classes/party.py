from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectId, ObjectIdRef
from intl_text import InternationalizedText


class Party(BaseModel):
    _type: Literal[TypeTags.PartyTag] = Field(TypeTags.PartyTag)
    _id: ObjectId
    abbreviation: Optional[str]
    is_recognized_party: bool = False
    leader_person_ids: List[ObjectIdRef] = []
    name: InternationalizedText

    class Config:
        alias_generator = fieldname_alias
