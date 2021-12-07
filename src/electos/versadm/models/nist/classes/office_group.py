from typing import Literal, List, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import ObjectIdRef, fieldname_alias


class OfficeGroup(BaseModel):
    obj_type: Literal[TypeTags.OfficeGroupTag] = Field(TypeTags.OfficeGroupTag)

    label: Optional[str]
    name: str
    office_ids: List[ObjectIdRef] = []
    sub_office_group: List['OfficeGroup'] = []

    class Config:
        alias_generator = fieldname_alias
