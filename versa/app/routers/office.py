from typing import List

from fastapi import APIRouter

from versa.api.api_request import ApiRequest
from versa.app.db.in_memory import InMemoryDb
from versa.app.routers.common import create_api_decorator
from versa.nist_model.classes.office import Office


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    @router.post('/offices')
    @request_handler
    def create_office(req: ApiRequest[Office]) -> str:
        return app_state.offices.put(req.data, overwrite=False)

    @router.get('/offices')
    @request_handler
    def get_offices() -> List[Office]:
        return app_state.offices.values()

    @router.put('/offices/{office_id}')
    @request_handler
    def update_office(office_id: str, req: ApiRequest[Office]) -> str:
        # check that the record exists before updating
        app_state.offices.get(office_id)
        return app_state.offices.put(req.data, overwrite=True)

    @router.delete('/offices/{office_id}')
    @request_handler
    def delete_office(office_id: str) -> bool:
        return app_state.offices.delete(office_id)

    return router
