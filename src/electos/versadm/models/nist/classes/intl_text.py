from typing import List, Literal

from pydantic import BaseModel, Field

from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias


class LanguageString(BaseModel):
    obj_type: Literal[TypeTags.LanguageStringTag] = Field(TypeTags.LanguageStringTag)

    content: str
    language: str

    class Config:
        alias_generator = fieldname_alias


class InternationalizedText(BaseModel):
    obj_type: Literal[TypeTags.InternationalizedTextTag] = Field(TypeTags.InternationalizedTextTag)

    text: List[LanguageString] = Field(..., min_items=1)

    class Config:
        alias_generator = fieldname_alias
