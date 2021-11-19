from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from pydantic.networks import AnyUrl

DataT = TypeVar('DataT')


class Error(BaseModel):
    code: str = Field(
        ..., description='Software-friendly identifier for the type of error.'
    )
    message: str = Field(
        ..., description='Human-friendly explanation of the error.'
    )


class ApiResponse(GenericModel, Generic[DataT]):
    errors: Optional[List[Error]] = Field(
        None,
        description='List of errors, if any, that occurred in the handling of the request.',
    )
    data: Optional[DataT] = Field(
        None,
        description='The payload for a successful response.'
    )
    changeId: str = Field(
        ...,
        description='An opaque fingerprint representing the state of the system after the request has been made.'
    )
    refId: UUID = Field(
        ...,
        description='Uniquely identifies the request-handling execution that produced this response, for '
                    'troubleshooting/auditing. This id is included in any service-side logs associated with the '
                    'request/response.',
    )


class ApiResponsePaginated(GenericModel, Generic[DataT]):
    errors: Optional[List[Error]] = Field(
        None,
        description='List of errors, if any, that occurred in the handling of the request.',
    )
    data: List[DataT] = Field(
        None,
        description='A page of results for a successful response.'
    )
    changeId: str = Field(
        ...,
        description='An opaque fingerprint representing the state of the system after the request has been made.'
    )
    refId: UUID = Field(
        ...,
        description='Uniquely identifies the request-handling execution that produced this response, for '
                    'troubleshooting/auditing. This id is included in any service-side logs associated with the '
                    'request/response.',
    )
    first: Optional[AnyUrl] = Field(
        None, description='URI for the first set of paginated results.'
    )
    prev: Optional[AnyUrl] = Field(
        None,
        description='URI for the previous set of paginated results. If blank or absent, there are no previous pages '
                    'of results available to fetch.',
    )
    next: Optional[AnyUrl] = Field(
        None,
        description='URI for the next set of paginated results. If blank or absent, there are no more pages of results '
                    'available to fetch.',
    )
    last: Optional[AnyUrl] = Field(
        None,
        description='URI for the last set of paginated results. May be the same as _first.',
    )
    page_max: Optional[int] = Field(
        None, description='Number of items in a complete page of results.'
    )
    total_results: Optional[int] = Field(
        None,
        description='Total number of results available to fetch across all pages. May be blank or absent if '
                    'this number is difficult or costly to compute.',
    )
