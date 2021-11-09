from typing import List
from uuid import uuid4

from fastapi import APIRouter

from versa.api.api_request import ApiRequest
from versa.api.api_response import ApiResponse
from versa.app.db.in_memory import InMemoryDb
from versa.nist_model.classes.party import Party


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    @router.post('/parties')
    def create_party(req: ApiRequest[Party]) -> str:
        party_id = app_state.parties.put(req.data, overwrite=False)
        return party_id

    @router.get('/parties')
    def get_parties() -> ApiResponse[List[Party]]:
        return ApiResponse(
            _changeId=app_state.hash_state(),
            _refId=uuid4().hex,
            data=list(app_state.parties.values())
        )

    @router.put('/parties/{id}')
    def update_party(id: str, req: ApiRequest[Party]) -> str:
        # check that the record exists before updating
        app_state.parties.get(id)
        party_id = app_state.parties.put(req.data, overwrite=True)
        return party_id

    @router.delete('/parties/{id}')
    def delete_party(id: str) -> bool:
        return app_state.parties.delete(id)

    return router
