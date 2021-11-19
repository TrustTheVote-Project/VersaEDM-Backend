from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .external_identifier import ExternalIdentifier
from .intl_text import InternationalizedText
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef


class BallotMeasureSelection(BaseModel):
    obj_type: Literal[TypeTags.BallotMeasureSelectionTag] = Field(TypeTags.BallotMeasureSelectionTag)

    external_identifier: List[ExternalIdentifier] = []
    selection: InternationalizedText
    sequence_order: Optional[int]

    class Config:
        alias_generator = fieldname_alias


class CandidateSelection(BaseModel):
    obj_type: Literal[TypeTags.CandidateSelectionTag] = Field(TypeTags.CandidateSelectionTag)

    candidate_ids: List[ObjectIdRef]
    endorsement_party_ids: List[ObjectIdRef] = []
    is_write_in: bool = False
    sequence_order: Optional[int]

    class Config:
        alias_generator = fieldname_alias
