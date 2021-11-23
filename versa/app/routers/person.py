from typing import List

from fastapi import APIRouter

from versa.api.api_request import ApiRequest
from versa.app.db.in_memory import InMemoryDb
from versa.app.routers.common import create_api_decorator
from versa.nist_model.classes.person import Person


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    @router.post('/persons')
    @request_handler
    def create_person(req: ApiRequest[Person]) -> str:
        person_id = app_state.persons.put(req.data, overwrite=False)
        return person_id

    @router.get('/persons')
    @request_handler
    def get_persons() -> List[Person]:
        return app_state.persons.values()

    @router.put('/persons/{person_id}')
    @request_handler
    def update_person(person_id: str, req: ApiRequest[Person]) -> str:
        # check that the record exists before updating
        app_state.persons.get(person_id)
        person_id = app_state.persons.put(req.data, overwrite=True)
        return person_id

    @router.delete('/persons/{person_id}')
    @request_handler
    def delete_person(person_id: str) -> bool:
        return app_state.persons.delete(person_id)

    return router
