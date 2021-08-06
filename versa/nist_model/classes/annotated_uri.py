from enum import Enum
from pydantic import AnyUrl, BaseModel, Field
from typing import Literal, Optional


class AnnotatedUri(BaseModel):
    class TypeTag(str, Enum):
        TYPE = 'ElectionResults.AnnotatedUri'

    class Config:
        allow_population_by_field_name = True

    obj_type: Literal[TypeTag.TYPE] = Field(default=TypeTag.TYPE, alias='@type')
    content: AnyUrl = Field(
        ...,
        alias='Content',
        description="The URI to which the annotation applies."
    )
    annotation: Optional[str] = Field(
        None,
        alias='Annotation',
        description="The text of the annotation.",
        max_length=32
    )
