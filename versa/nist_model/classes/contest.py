from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .annotated_uri import AnnotatedUri
from .contest_selection import BallotMeasureSelection, CandidateSelection
from .intl_text import InternationalizedText
from ..enums.nist import VoteVariationEnum, BallotMeasureContestTypeEnum
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectId, ObjectIdRef


class BallotMeasureContest(BaseModel):
    obj_type: Literal[TypeTags.BallotMeasureContestTag] = Field(TypeTags.BallotMeasureContestTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    ballot_sub_title: Optional[InternationalizedText]
    ballot_title: Optional[InternationalizedText]
    con_statement: Optional[InternationalizedText]
    contest_selection: List[BallotMeasureSelection] = []
    contest_type: Optional[BallotMeasureContestTypeEnum] = Field(None, alias='Type')
    effect_of_abstain: Optional[InternationalizedText]
    election_district_id: ObjectIdRef
    full_text: Optional[InternationalizedText]
    has_rotation: bool = False
    info_uri: Optional[AnnotatedUri]
    name: str
    other_type: Optional[str]
    other_vote_variation: Optional[str]
    passage_threshold: Optional[InternationalizedText]
    pro_statement: Optional[InternationalizedText]
    sequence_order: Optional[int]
    summary_text: Optional[InternationalizedText]
    vote_variation: Optional[VoteVariationEnum]

    class Config:
        alias_generator = fieldname_alias


class CandidateContest(BaseModel):
    obj_type: Literal[TypeTags.CandidateContestTag] = Field(TypeTags.CandidateContestTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    ballot_sub_title: Optional[InternationalizedText]
    ballot_title: Optional[InternationalizedText]
    contest_selection: List[CandidateSelection] = []
    election_district_id: ObjectIdRef
    has_rotation: bool = False
    name: str
    number_elected: Optional[int] = Field(None, ge=0)
    number_runoff: Optional[int] = Field(None, ge=0)
    office_ids: List[ObjectIdRef] = []
    other_vote_variation: Optional[str]
    primary_party_ids: List[ObjectIdRef] = []
    sequence_order: Optional[int]
    vote_variation: Optional[VoteVariationEnum]
    votes_allowed: Optional[int] = Field(None, ge=0)

    class Config:
        alias_generator = fieldname_alias
