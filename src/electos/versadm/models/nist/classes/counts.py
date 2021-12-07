from typing import Literal, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.device_class import DeviceClass
from versadm.models.nist.enums.nist import CountItemTypeEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias, ObjectIdRef


class BallotCounts(BaseModel):
    obj_type: Literal[TypeTags.BallotCountsTag] = Field(TypeTags.BallotCountsTag)

    ballots_cast: Optional[int]
    ballots_outstanding: Optional[int]
    ballots_rejected: Optional[int]
    counts_type: CountItemTypeEnum = Field(..., alias='Type')
    device_class: Optional[DeviceClass]
    gp_unit_id: ObjectIdRef
    is_suppressed_for_privacy: bool = False
    other_type: Optional[str]
    round: Optional[int]


class OtherCounts(BaseModel):
    obj_type: Literal[TypeTags.OtherCountsTag] = Field(TypeTags.OtherCountsTag)

    device_class: Optional[DeviceClass]
    gp_unit_id: ObjectIdRef
    overvotes: Optional[float]
    undervotes: Optional[float]
    write_ins: Optional[float]

    class Config:
        alias_generator = fieldname_alias


class VoteCounts(BaseModel):
    obj_type: Literal[TypeTags.VoteCountsTag] = Field(TypeTags.VoteCountsTag)

    count: float
    counts_type: CountItemTypeEnum = Field(..., alias='Type')
    device_class: Optional[DeviceClass]
    gp_unit_id: ObjectIdRef
    is_suppressed_for_privacy: bool = False
    other_type: Optional[str]
    round: Optional[int]

    class Config:
        alias_generator = fieldname_alias
