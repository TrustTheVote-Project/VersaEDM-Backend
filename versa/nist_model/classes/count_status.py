from typing import Literal, Optional

from pydantic import BaseModel, Field

from versa.nist_model.enums.nist import CountItemStatusEnum, CountItemTypeEnum
from versa.nist_model.enums.type_tag import TypeTags
from versa.nist_model.util import fieldname_alias


class CountStatus(BaseModel):
    obj_type: Literal[TypeTags.CountStatusTag] = Field(TypeTags.CountStatusTag)

    other_type: Optional[str]
    status: CountItemStatusEnum
    count_status_type: CountItemTypeEnum = Field(..., alias='Type')

    class Config:
        alias_generator = fieldname_alias
