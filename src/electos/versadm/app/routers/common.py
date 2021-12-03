import functools
from typing import Callable
from uuid import uuid4

from versadm.api.api_response import ApiResponse
from versadm.app.db.in_memory import InMemoryDb


def create_api_decorator(app_state: InMemoryDb) -> Callable:
    def request_handler(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> ApiResponse:
            # TODO: handle exceptions and turn them into HTTP/API errors according to the spec
            func_result = func(*args, **kwargs)
            return ApiResponse(
                changeId=app_state.hash_state(),
                refId=uuid4().hex,
                data=func_result
            )
        return wrapped
    return request_handler
