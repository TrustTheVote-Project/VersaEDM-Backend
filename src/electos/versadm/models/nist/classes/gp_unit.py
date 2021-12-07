from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.contact_information import ContactInformation
from versadm.models.nist.classes.count_status import CountStatus
from versadm.models.nist.classes.device_class import DeviceClass
from versadm.models.nist.classes.election_administration import ElectionAdministration
from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.intl_text import InternationalizedText
from versadm.models.nist.classes.party_registration import PartyRegistration
from versadm.models.nist.classes.spatial_dimension import SpatialDimension
from versadm.models.nist.enums.nist import ReportingUnitTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectId, ObjectIdRef


class ReportingUnit(BaseModel):
    obj_type: Literal[TypeTags.ReportingUnitTag] = Field(TypeTags.ReportingUnitTag)
    obj_id: ObjectId

    authority_ids: List[ObjectIdRef] = []
    composing_gp_unit_ids: List[ObjectIdRef] = []
    contact_information: Optional[ContactInformation]
    count_status: List[CountStatus] = []
    election_administration: Optional[ElectionAdministration]
    external_identifier: List[ExternalIdentifier] = []
    is_districted: bool = False
    is_mail_only: bool = False
    name: Optional[InternationalizedText]
    number: Optional[str]
    other_type: Optional[str]
    party_registration: List[PartyRegistration] = []
    reporting_unit_type: ReportingUnitTypeEnum = Field(..., alias='Type')
    spatial_dimension: Optional[SpatialDimension]
    sub_units_reported: Optional[int]
    total_sub_units: Optional[int]
    voters_participated: Optional[int]
    voters_registered: Optional[int]

    class Config:
        alias_generator = fieldname_alias


class ReportingDevice(BaseModel):
    obj_type: Literal[TypeTags.ReportingDeviceTag] = Field(TypeTags.ReportingDeviceTag)
    obj_id: ObjectId

    composing_gp_unit_ids: List[ObjectIdRef] = []  # REVISIT: Is this meaningful for ReportingDevice?
    device_class: Optional[DeviceClass]
    external_identifier: List[ExternalIdentifier] = []
    name: Optional[InternationalizedText]
    serial_number: Optional[str]
