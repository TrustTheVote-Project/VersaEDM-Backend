from datetime import date
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .ballot_style import BallotStyle
from .candidate import Candidate
from .contest import BallotMeasureContest, CandidateContest
from .intl_text import InternationalizedText
from ..enums.nist import ElectionTypeEnum
from ..enums.type_tag import TypeTags
from ..util import fieldname_alias, ObjectIdRef


class Election(BaseModel):
    obj_type: Literal[TypeTags.ElectionTag] = Field(TypeTags.ElectionTag)

    ballot_style: List[BallotStyle] = []
    candidate: List[Candidate] = []
    contest: List[Union[BallotMeasureContest, CandidateContest]] = []
    election_scope_id: ObjectIdRef
    end_date: date
    name: InternationalizedText
    other_type: Optional[str]
    start_date: date
    election_type: ElectionTypeEnum = Field(..., alias="Type")

    class Config:
        alias_generator = fieldname_alias
