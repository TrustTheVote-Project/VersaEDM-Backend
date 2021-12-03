from typing import Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.enums.nist import CountItemStatusEnum, CountItemTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias


class CountStatus(BaseModel):
    obj_type: Literal[TypeTags.CountStatusTag] = Field(TypeTags.CountStatusTag)

    other_type: Optional[str]
    status: CountItemStatusEnum
    count_status_type: CountItemTypeEnum = Field(..., alias='Type')

    class Config:
        alias_generator = fieldname_alias
