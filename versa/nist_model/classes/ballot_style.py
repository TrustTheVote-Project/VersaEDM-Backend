from typing import List, Literal, Union

from pydantic import BaseModel, Field

from .ordered_content import OrderedContest, OrderedHeader
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef


class BallotStyle(BaseModel):
    _type: Literal[TypeTags.BallotStyleTag] = Field(TypeTags.BallotStyleTag)
    gp_unit_ids: List[ObjectIdRef] = Field(..., min_items=1)
    ordered_content: List[Union[OrderedContest, OrderedHeader]] = []
    party_ids: List[ObjectIdRef] = []

    class Config:
        alias_generator = fieldname_alias
