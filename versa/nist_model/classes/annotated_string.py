from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal, Optional


class AnnotatedString(BaseModel):
    class TypeTag(str, Enum):
        TYPE = 'ElectionResults.AnnotatedString'

    class Config:
        allow_population_by_field_name = True

    obj_type: Literal[TypeTag.TYPE] = Field(default=TypeTag.TYPE, alias='@type')
    content: str = Field(
        ...,
        alias='Content',
        description="The text to which the annotation applies."
    )
    annotation: Optional[str] = Field(
        None,
        alias='Annotation',
        description="The text of the annotation.",
        max_length=32
    )
