from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .election import Election
from .external_identifier import ExternalIdentifier
from .gp_unit import ReportingUnit
from .office import Office
from .party import Party
from .person import Person
from ..enums.nist import ReportDetailLevelEnum, ResultsStatusEnum
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias


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
