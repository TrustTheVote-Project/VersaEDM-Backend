from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from versadm.models.nist.classes.election import Election
from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.gp_unit import ReportingUnit, ReportingDevice
from versadm.models.nist.classes.header import Header
from versadm.models.nist.classes.office import Office
from versadm.models.nist.classes.office_group import OfficeGroup
from versadm.models.nist.classes.party import Party, Coalition
from versadm.models.nist.classes.person import Person
from versadm.models.nist.enums.nist import ReportDetailLevelEnum, ResultsStatusEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias


class ElectionReport(BaseModel):
    obj_type: Literal[TypeTags.ElectionReportTag] = Field(TypeTags.ElectionReportTag)

    election: List[Election] = []
    external_identifier: List[ExternalIdentifier] = []
    format: ReportDetailLevelEnum
    generated_date: datetime
    gp_unit: List[Union[ReportingDevice, ReportingUnit]] = []
    header: List[Header] = []
    is_test: bool = False
    issuer: str
    issuer_abbreviation: str
    notes: Optional[str]
    office: List[Office] = []
    office_group: List[OfficeGroup] = []
    party: List[Union[Coalition, Party]] = []
    person: List[Person] = []
    sequence_end: int
    sequence_start: int
    status: ResultsStatusEnum
    test_type: Optional[str]
    vendor_application_id: str

    class Config:
        alias_generator = fieldname_alias
