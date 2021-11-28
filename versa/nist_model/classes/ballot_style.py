from typing import List, Literal, Union

from pydantic import BaseModel, Field

from .annotated_uri import AnnotatedUri
from .external_identifier import ExternalIdentifier
from .ordered_content import OrderedContest, OrderedHeader
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef


class BallotStyle(BaseModel):
    obj_type: Literal[TypeTags.BallotStyleTag] = Field(TypeTags.BallotStyleTag)

    external_identifier: List[ExternalIdentifier] = []
    gp_unit_ids: List[ObjectIdRef] = Field(..., min_items=1)
    image_uri: List[AnnotatedUri] = []
    ordered_content: List[Union[OrderedContest, OrderedHeader]] = []
    party_ids: List[ObjectIdRef] = []

    class Config:
        alias_generator = fieldname_alias
