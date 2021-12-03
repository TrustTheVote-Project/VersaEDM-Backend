from typing import Generic, Optional, TypeVar
from uuid import UUID

from pydantic import Field
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class ApiRequest(GenericModel, Generic[DataT]):
    data: Optional[DataT] = Field(
        None,
        description='The payload for the request.'
    )
    _refId: Optional[UUID] = None
