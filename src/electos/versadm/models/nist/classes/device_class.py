from typing import Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.enums.nist import DeviceTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias


class DeviceClass(BaseModel):
    obj_type: Literal[TypeTags.DeviceClassTag] = Field(TypeTags.DeviceClassTag)

    manufacturer: Optional[str]
    model: Optional[str]
    other_type: Optional[str]
    device_class_type: Optional[DeviceTypeEnum] = Field(None, alias='Type')

    class Config:
        alias_generator = fieldname_alias
