from typing import List, Literal, Union

from pydantic import BaseModel, Field

from versadm.models.nist.classes.annotated_uri import AnnotatedUri
from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.ordered_content import OrderedContest, OrderedHeader
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectIdRef


class BallotStyle(BaseModel):
    obj_type: Literal[TypeTags.BallotStyleTag] = Field(TypeTags.BallotStyleTag)

    external_identifier: List[ExternalIdentifier] = []
    gp_unit_ids: List[ObjectIdRef] = Field(..., min_items=1)
    image_uri: List[AnnotatedUri] = []
    ordered_content: List[Union[OrderedContest, OrderedHeader]] = []
    party_ids: List[ObjectIdRef] = []

    class Config:
        alias_generator = fieldname_alias
