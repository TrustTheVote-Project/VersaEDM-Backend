from typing import List, Literal, Optional

from pydantic import BaseModel, Field, constr

from versadm.models.nist.classes.annotated_uri import AnnotatedUri
from versadm.models.nist.classes.contact_information import ContactInformation
from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.intl_text import InternationalizedText
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectId, ObjectIdRef


class Party(BaseModel):
    obj_type: Literal[TypeTags.PartyTag] = Field(TypeTags.PartyTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    color: Optional[constr(regex=r'[0-9a-f]{6}')]
    contact_information: Optional[ContactInformation]
    external_identifier: List[ExternalIdentifier] = []
    is_recognized_party: bool = False
    leader_person_ids: List[ObjectIdRef] = []
    logo_uri: Optional[AnnotatedUri]
    name: InternationalizedText
    party_scope_gp_unit_ids: List[ObjectIdRef] = []
    slogan: Optional[InternationalizedText]

    class Config:
        alias_generator = fieldname_alias


class Coalition(BaseModel):
    obj_type: Literal[TypeTags.CoalitionTag] = Field(TypeTags.CoalitionTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    color: Optional[constr(regex=r'[0-9a-f]{6}')]
    contact_information: Optional[ContactInformation]
    contest_ids: List[ObjectIdRef] = []
    external_identifier: List[ExternalIdentifier] = []
    is_recognized_party: bool = False
    leader_person_ids: List[ObjectIdRef] = []
    logo_uri: Optional[AnnotatedUri]
    name: InternationalizedText
    party_ids: List[ObjectIdRef]
    party_scope_gp_unit_ids: List[ObjectIdRef] = []
    slogan: Optional[InternationalizedText]

    class Config:
        alias_generator = fieldname_alias
