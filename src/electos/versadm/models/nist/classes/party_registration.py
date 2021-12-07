from typing import Literal

from pydantic import BaseModel, Field

from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectIdRef


class PartyRegistration(BaseModel):
    obj_type: Literal[TypeTags.PartyRegistrationTag] = Field(TypeTags.PartyRegistrationTag)

    count: int = Field(..., ge=0)
    party_id: ObjectIdRef

    class Config:
        alias_generator = fieldname_alias
