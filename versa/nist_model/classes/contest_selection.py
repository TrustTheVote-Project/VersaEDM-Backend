from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .external_identifier import ExternalIdentifier
from .intl_text import InternationalizedText
from .counts import VoteCounts
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef, ObjectId


class BallotMeasureSelection(BaseModel):
    obj_type: Literal[TypeTags.BallotMeasureSelectionTag] = Field(TypeTags.BallotMeasureSelectionTag)
    obj_id: ObjectId

    external_identifier: List[ExternalIdentifier] = []
    selection: InternationalizedText
    sequence_order: Optional[int]
    vote_counts: List[VoteCounts] = []

    class Config:
        alias_generator = fieldname_alias


class CandidateSelection(BaseModel):
    obj_type: Literal[TypeTags.CandidateSelectionTag] = Field(TypeTags.CandidateSelectionTag)
    obj_id: ObjectId

    candidate_ids: List[ObjectIdRef]
    endorsement_party_ids: List[ObjectIdRef] = []
    is_write_in: bool = False
    sequence_order: Optional[int]
    vote_counts: List[VoteCounts] = []

    class Config:
        alias_generator = fieldname_alias


class PartySelection(BaseModel):
    obj_type: Literal[TypeTags.PartySelectionTag] = Field(TypeTags.PartySelectionTag)
    obj_id: ObjectId

    party_ids: List[ObjectIdRef] = Field(..., min_items=1)
    sequence_order: Optional[int]
    vote_counts: List[VoteCounts] = []
