from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.annotated_uri import AnnotatedUri
from versadm.models.nist.classes.contest_selection import BallotMeasureSelection, CandidateSelection, PartySelection
from versadm.models.nist.classes.count_status import CountStatus
from versadm.models.nist.classes.counts import OtherCounts
from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.intl_text import InternationalizedText
from versadm.models.nist.enums.nist import VoteVariationEnum, BallotMeasureContestTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectId, ObjectIdRef


class BallotMeasureContest(BaseModel):
    obj_type: Literal[TypeTags.BallotMeasureContestTag] = Field(TypeTags.BallotMeasureContestTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    ballot_sub_title: Optional[InternationalizedText]
    ballot_title: Optional[InternationalizedText]
    con_statement: Optional[InternationalizedText]
    contest_selection: List[BallotMeasureSelection] = []
    contest_type: Optional[BallotMeasureContestTypeEnum] = Field(None, alias='Type')
    count_status: List[CountStatus] = []
    effect_of_abstain: Optional[InternationalizedText]
    election_district_id: ObjectIdRef
    external_identifier: List[ExternalIdentifier] = []
    full_text: Optional[InternationalizedText]
    has_rotation: bool = False
    info_uri: List[AnnotatedUri] = []
    name: str
    other_counts: List[OtherCounts] = []
    other_type: Optional[str]
    other_vote_variation: Optional[str]
    passage_threshold: Optional[InternationalizedText]
    pro_statement: Optional[InternationalizedText]
    sequence_order: Optional[int]
    sub_units_reported: Optional[int]
    summary_text: Optional[InternationalizedText]
    total_sub_units: Optional[int]
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
    count_status: List[CountStatus] = []
    election_district_id: ObjectIdRef
    external_identifier: List[ExternalIdentifier] = []
    has_rotation: bool = False
    name: str
    number_elected: Optional[int] = Field(None, ge=0)
    number_runoff: Optional[int] = Field(None, ge=0)
    office_ids: List[ObjectIdRef] = []
    other_counts: List[OtherCounts] = []
    other_vote_variation: Optional[str]
    primary_party_ids: List[ObjectIdRef] = []
    sequence_order: Optional[int]
    sub_units_reported: Optional[int]
    total_sub_units: Optional[int]
    vote_variation: Optional[VoteVariationEnum]
    votes_allowed: int = Field(..., ge=0)

    class Config:
        alias_generator = fieldname_alias


class PartyContest(BaseModel):
    obj_type: Literal[TypeTags.PartyContestTag] = Field(TypeTags.PartyContestTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    ballot_sub_title: Optional[InternationalizedText]
    ballot_title: Optional[InternationalizedText]
    contest_selection: List[PartySelection] = []
    count_status: List[CountStatus] = []
    election_district_id: ObjectIdRef
    external_identifier: List[ExternalIdentifier] = []
    has_rotation: bool = False
    name: str
    other_counts: List[OtherCounts] = []
    other_vote_variation: Optional[str]
    sequence_order: Optional[int]
    sub_units_reported: Optional[int]
    total_sub_units: Optional[int]
    vote_variation: Optional[VoteVariationEnum]

    class Config:
        alias_generator = fieldname_alias


class RetentionContest(BaseModel):
    obj_type: Literal[TypeTags.RetentionContestTag] = Field(TypeTags.RetentionContestTag)
    obj_id: ObjectId

    abbreviation: Optional[str]
    ballot_sub_title: Optional[InternationalizedText]
    ballot_title: Optional[InternationalizedText]
    candidate_id: ObjectIdRef
    con_statement: Optional[InternationalizedText]
    # BallotMeasureSelection is intentional here, following the NIST spec (single candidate with retain/no-retain opts)
    contest_selection: List[BallotMeasureSelection] = []
    # BallotMeasureContestType is intentional here, following the NIST spec (no separate type for RetentionContest)
    contest_type: Optional[BallotMeasureContestTypeEnum] = Field(None, alias='Type')
    count_status: List[CountStatus] = []
    effect_of_abstain: Optional[InternationalizedText]
    election_district_id: ObjectIdRef
    external_identifier: List[ExternalIdentifier] = []
    full_text: Optional[InternationalizedText]
    has_rotation: bool = False
    info_uri: List[AnnotatedUri] = []
    name: str
    office_id: Optional[ObjectIdRef]
    other_counts: List[OtherCounts] = []
    other_type: Optional[str]
    other_vote_variation: Optional[str]
    passage_threshold: Optional[InternationalizedText]
    pro_statement: Optional[InternationalizedText]
    sequence_order: Optional[int]
    sub_units_reported: Optional[int]
    summary_text: Optional[InternationalizedText]
    total_sub_units: Optional[int]
    vote_variation: Optional[VoteVariationEnum]

    class Config:
        alias_generator = fieldname_alias
