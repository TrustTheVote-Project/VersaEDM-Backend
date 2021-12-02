from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from versa.nist_model.classes.election import Election
from versa.nist_model.classes.external_identifier import ExternalIdentifier
from versa.nist_model.classes.gp_unit import ReportingUnit
from versa.nist_model.classes.office import Office
from versa.nist_model.classes.party import Party
from versa.nist_model.classes.person import Person
from versa.nist_model.enums.nist import ReportDetailLevelEnum, ResultsStatusEnum
from versa.nist_model.enums.type_tag import TypeTags
from versa.nist_model.util import fieldname_alias


class ElectionReport(BaseModel):
    obj_type: Literal[TypeTags.ElectionReportTag] = Field(TypeTags.ElectionReportTag)

    election: List[Election] = []
    external_identifier: List[ExternalIdentifier] = []
    format: ReportDetailLevelEnum
    generated_date: datetime
    gp_unit: List[Union[ReportingUnit]] = []
    is_test: bool = False
    issuer: str
    issuer_abbreviation: str
    office: List[Office] = []
    party: List[Party] = []
    person: List[Person] = []
    sequence_end: int
    sequence_start: int
    status: ResultsStatusEnum
    test_type: Optional[str]
    vendor_application_id: str

    class Config:
        alias_generator = fieldname_alias
