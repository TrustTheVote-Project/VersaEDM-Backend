from typing import List

from fastapi import APIRouter

from versa.api.api_request import ApiRequest
from versa.app.db.in_memory import InMemoryDb
from versa.app.routers.common import create_api_decorator
from versa.nist_model.classes.party import Party


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    @router.post('/parties')
    @request_handler
    def create_party(req: ApiRequest[Party]) -> str:
        party_id = app_state.parties.put(req.data, overwrite=False)
        return party_id

    @router.get('/parties')
    @request_handler
    def get_parties() -> List[Party]:
        return list(app_state.parties.values())

    @router.put('/parties/{party_id}')
    @request_handler
    def update_party(party_id: str, req: ApiRequest[Party]) -> str:
        # check that the record exists before updating
        app_state.parties.get(party_id)
        party_id = app_state.parties.put(req.data, overwrite=True)
        return party_id

    @router.delete('/parties/{party_id}')
    @request_handler
    def delete_party(party_id: str) -> bool:
        return app_state.parties.delete(party_id)

    return router
