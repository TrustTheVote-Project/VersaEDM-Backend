from datetime import date
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from versadm.models.nist.classes.ballot_style import BallotStyle
from versadm.models.nist.classes.candidate import Candidate
from versadm.models.nist.classes.contact_information import ContactInformation
from versadm.models.nist.classes.contest import BallotMeasureContest, CandidateContest, PartyContest, RetentionContest
from versadm.models.nist.classes.count_status import CountStatus
from versadm.models.nist.classes.counts import BallotCounts
from versadm.models.nist.classes.external_identifier import ExternalIdentifier
from versadm.models.nist.classes.intl_text import InternationalizedText
from versadm.models.nist.enums.nist import ElectionTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectIdRef


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
