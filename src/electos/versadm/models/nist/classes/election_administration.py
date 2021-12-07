from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.contact_information import ContactInformation
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectIdRef


class ElectionAdministration(BaseModel):
    obj_type: Literal[TypeTags.ElectionAdministrationTag] = Field(TypeTags.ElectionAdministrationTag)

    contact_information: Optional[ContactInformation]
    election_official_person_ids: List[ObjectIdRef] = []
    name: Optional[str]

    class Config:
        alias_generator = fieldname_alias
