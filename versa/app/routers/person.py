from typing import List
from uuid import uuid4

from fastapi import APIRouter

from versa.api.api_request import ApiRequest
from versa.api.api_response import ApiResponse
from versa.app.db.in_memory import InMemoryDb
from versa.nist_model.classes.person import Person


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    @router.post('/persons')
    def create_person(req: ApiRequest[Person]) -> str:
        person_id = app_state.persons.put(req.data, overwrite=False)
        return person_id

    @router.get('/persons')
    def get_persons() -> ApiResponse[List[Person]]:
        return ApiResponse(
            _changeId=app_state.hash_state(),
            _refId=uuid4().hex,
            data=list(app_state.persons.values())
        )

    @router.put('/persons/{id}')
    def update_person(id: str, req: ApiRequest[Person]) -> str:
        # check that the record exists before updating
        app_state.persons.get(id)
        person_id = app_state.persons.put(req.data, overwrite=True)
        return person_id

    @router.delete('/persons/{id}')
    def delete_person(id: str) -> bool:
        return app_state.persons.delete(id)

    return router
