from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.enums.nist import ReportingUnitTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectId, ObjectIdRef


class ReportingUnit(BaseModel):
    obj_type: Literal[TypeTags.ReportingUnitTag] = Field(TypeTags.ReportingUnitTag)
    obj_id: ObjectId

    authority_ids: List[ObjectIdRef] = []
    composing_gp_unit_ids: List[ObjectIdRef] = []
    external_identifier: List[ExternalIdentifier] = []
    is_districted: bool = False
    is_mail_only: bool = False
    name: Optional[str]
    reporting_unit_type: ReportingUnitTypeEnum = Field(..., alias='Type')
    other_type: Optional[str]

    class Config:
        alias_generator = fieldname_alias