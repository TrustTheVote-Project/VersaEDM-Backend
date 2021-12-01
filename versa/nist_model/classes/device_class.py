from typing import Literal, Optional

from pydantic import BaseModel, Field

from versa.nist_model.enums.nist import DeviceTypeEnum
from versa.nist_model.enums.type_tag import TypeTags
from versa.nist_model.util import fieldname_alias


class DeviceClass(BaseModel):
    obj_type: Literal[TypeTags.DeviceClassTag] = Field(TypeTags.DeviceClassTag)

    manufacturer: Optional[str]
    model: Optional[str]
    other_type: Optional[str]
    device_class_type: DeviceTypeEnum = Field(..., alias='Type')

    class Config:
        alias_generator = fieldname_alias
