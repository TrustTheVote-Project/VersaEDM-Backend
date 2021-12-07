from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.contact_information import ContactInformation
from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.intl_text import InternationalizedText
from versadm.models.nist.enums.nist import OfficeTermTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectId, ObjectIdRef


class Term(BaseModel):
    obj_type: Literal[TypeTags.TermTag] = Field(TypeTags.TermTag)

    end_date: Optional[date]
    label: Optional[str]
    start_date: Optional[date]
    office_term_type: Optional[OfficeTermTypeEnum]


class Office(BaseModel):
    obj_type: Literal[TypeTags.OfficeTag] = Field(TypeTags.OfficeTag)
    obj_id: ObjectId

    contact_information: Optional[ContactInformation]
    description: Optional[InternationalizedText]
    election_district_id: Optional[ObjectIdRef]
    external_identifier: List[ExternalIdentifier] = []
    filing_deadline: Optional[date]
    is_partisan: bool = True
    name: InternationalizedText
    office_holder_person_ids: List[ObjectIdRef] = []
    term: Optional[Term]

    class Config:
        alias_generator = fieldname_alias
