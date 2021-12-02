from datetime import date
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from versa.nist_model.classes.ballot_style import BallotStyle
from versa.nist_model.classes.candidate import Candidate
from versa.nist_model.classes.contact_information import ContactInformation
from versa.nist_model.classes.contest import BallotMeasureContest, CandidateContest, PartyContest, RetentionContest
from versa.nist_model.classes.count_status import CountStatus
from versa.nist_model.classes.counts import BallotCounts
from versa.nist_model.classes.external_identifier import ExternalIdentifier
from versa.nist_model.classes.intl_text import InternationalizedText
from versa.nist_model.enums.nist import ElectionTypeEnum
from versa.nist_model.enums.type_tag import TypeTags
from versa.nist_model.util import fieldname_alias, ObjectIdRef


class Election(BaseModel):
    obj_type: Literal[TypeTags.ElectionTag] = Field(TypeTags.ElectionTag)

    ballot_counts: List[BallotCounts] = []
    ballot_style: List[BallotStyle] = []
    candidate: List[Candidate] = []
    contact_information: Optional[ContactInformation]
    contest: List[Union[BallotMeasureContest, CandidateContest, PartyContest, RetentionContest]] = []
    count_status: List[CountStatus] = []
    election_scope_id: ObjectIdRef
    end_date: date
    external_identifier: List[ExternalIdentifier] = []
    name: InternationalizedText
    other_type: Optional[str]
    start_date: date
    election_type: ElectionTypeEnum = Field(..., alias="Type")

    class Config:
        alias_generator = fieldname_alias
