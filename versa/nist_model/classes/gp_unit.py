from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from versa.nist_model.classes.external_identifier import ExternalIdentifier
from versa.nist_model.enums.nist import ReportingUnitTypeEnum
from versa.nist_model.enums.type_tag import TypeTags
from versa.nist_model.util import fieldname_alias, ObjectId, ObjectIdRef


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
