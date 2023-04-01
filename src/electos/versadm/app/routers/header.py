from typing import List

from fastapi import APIRouter

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.header import Header


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    @router.post('/headers')
    @request_handler
    def create_header(req: ApiRequest[Header]) -> str:
        return app_state.headers.put(req.data, overwrite=False)

    @router.get('/headers')
    @request_handler
    def get_headers() -> List[Header]:
        return app_state.headers.values()

    @router.get('/headers/{header_id}')
    @request_handler
    def get_header(header_id: str) -> Header:
        return app_state.headers.get(header_id)

    @router.put('/headers/{header_id}')
    @request_handler
    def update_header(header_id: str, req: ApiRequest[Header]) -> str:
        # check that the record exists before updating
        app_state.headers.get(header_id)
        return app_state.headers.put(req.data, overwrite=True)

    @router.delete('/headers/{header_id}')
    @request_handler
    def delete_header(header_id: str) -> bool:
        return app_state.headers.delete(header_id)

    return router
