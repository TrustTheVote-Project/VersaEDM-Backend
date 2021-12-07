from typing import Literal, List

from pydantic import BaseModel, Field

from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.intl_text import InternationalizedText
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import ObjectId, fieldname_alias


class Header(BaseModel):
    obj_type: Literal[TypeTags.HeaderTag] = Field(TypeTags.HeaderTag)
    obj_id: ObjectId

    external_identifier: List[ExternalIdentifier] = []
    name: InternationalizedText

    class Config:
        alias_generator = fieldname_alias
