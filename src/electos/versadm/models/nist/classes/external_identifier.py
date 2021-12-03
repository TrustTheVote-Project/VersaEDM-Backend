from typing import Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.enums.nist import ExternalIdentifierType
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias


class ExternalIdentifier(BaseModel):
    obj_type: Literal[TypeTags.ExternalIdentifierTag] = Field(TypeTags.ExternalIdentifierTag)

    label: Optional[str]
    external_identifier_type: ExternalIdentifierType = Field(..., alias='Type')
    other_type: Optional[str]
    value: str

    class Config:
        alias_generator = fieldname_alias
