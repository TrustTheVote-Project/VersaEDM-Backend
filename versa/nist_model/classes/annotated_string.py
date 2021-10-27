from typing import Literal, Optional

from pydantic import BaseModel, Field

from versa.nist_model.enums.type_tag import TypeTags
from versa.nist_model.util import fieldname_alias


class AnnotatedString(BaseModel):
    class Config:
        alias_generator = fieldname_alias

    _type: Literal[TypeTags.AnnotatedStringTag] = Field(TypeTags.AnnotatedStringTag)
    content: str
    annotation: Optional[str] = Field(
        None,
        max_length=32
    )
