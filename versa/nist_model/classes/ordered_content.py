from typing import List, Literal, Union

from pydantic import BaseModel, Field

from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef


class OrderedContest(BaseModel):
    _type: Literal[TypeTags.OrderedContestTag] = Field(TypeTags.OrderedContestTag)
    contest_id: ObjectIdRef
    ordered_contest_selection_ids: List[ObjectIdRef]

    class Config:
        alias_generator = fieldname_alias


class OrderedHeader(BaseModel):
    _type: Literal[TypeTags.OrderedHeaderTag] = Field(TypeTags.OrderedHeaderTag)
    header_id: ObjectIdRef
    ordered_content: List[Union[OrderedContest, 'OrderedHeader']] = []
