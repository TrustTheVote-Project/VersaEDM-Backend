from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef
from .intl_text import InternationalizedText


class BallotMeasureSelection(BaseModel):
    _type: Literal[TypeTags.BallotMeasureSelectionTag] = Field(TypeTags.BallotMeasureSelectionTag)
    selection: InternationalizedText
    sequence_order: Optional[int]

    class Config:
        alias_generator = fieldname_alias


class CandidateSelection(BaseModel):
    _type: Literal[TypeTags.CandidateSelectionTag] = Field(TypeTags.CandidateSelectionTag)
    candidate_ids: List[ObjectIdRef]
    endorsement_party_ids: List[ObjectIdRef] = []
    is_write_in: bool = False
    sequence_order: Optional[int]

    class Config:
        alias_generator = fieldname_alias
