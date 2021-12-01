from datetime import date
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .ballot_style import BallotStyle
from .candidate import Candidate
from .contact_information import ContactInformation
from .contest import BallotMeasureContest, CandidateContest, PartyContest, RetentionContest
from .count_status import CountStatus
from .counts import BallotCounts
from .external_identifier import ExternalIdentifier
from .intl_text import InternationalizedText
from ..enums.nist import ElectionTypeEnum
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef


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
