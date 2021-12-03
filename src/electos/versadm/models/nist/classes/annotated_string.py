from typing import Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias


class AnnotatedString(BaseModel):
    class Config:
        alias_generator = fieldname_alias

    obj_type: Literal[TypeTags.AnnotatedStringTag] = Field(TypeTags.AnnotatedStringTag)

    content: str
    annotation: Optional[str] = Field(
        None,
        max_length=32
    )
