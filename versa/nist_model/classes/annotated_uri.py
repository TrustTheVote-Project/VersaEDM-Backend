from pydantic import AnyUrl, BaseModel, Field
from typing import Literal, Optional

from versa.nist_model.enums.type_tag import TypeTags
from versa.nist_model.util import fieldname_alias


class AnnotatedUri(BaseModel):
    class Config:
        alias_generator = fieldname_alias

    _type: Literal[TypeTags.AnnotatedUriTag] = Field(TypeTags.AnnotatedUriTag)
    content: AnyUrl
    annotation: Optional[str] = Field(
        None,
        max_length=32
    )
