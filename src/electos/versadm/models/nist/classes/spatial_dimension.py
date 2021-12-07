from typing import Literal, List, Optional

from pydantic import BaseModel, Field

from versadm.models.nist.classes.annotated_uri import AnnotatedUri
from versadm.models.nist.enums.nist import GeoSpatialFormatEnum
from versadm.models.nist.enums.type_tag import TypeTags
from versadm.models.nist.util import fieldname_alias


class SpatialExtent(BaseModel):
    obj_type: Literal[TypeTags.SpatialExtentTag] = Field(TypeTags.SpatialExtentTag)

    coordinates: str
    format: GeoSpatialFormatEnum

    class Config:
        alias_generator = fieldname_alias


class SpatialDimension(BaseModel):
    obj_type: Literal[TypeTags.SpatialDimensionTag] = Field(TypeTags.SpatialDimensionTag)

    map_uri: List[AnnotatedUri] = []
    spatial_extent: Optional[SpatialExtent]

    class Config:
        alias_generator = fieldname_alias
