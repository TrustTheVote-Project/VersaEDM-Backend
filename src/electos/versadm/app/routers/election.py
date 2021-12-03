from typing import List

from fastapi import APIRouter

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.election import Election


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    def _validate_election(election: Election):
        # we require at least one external identifier since the schema doesn't define an @id but we need to identify it
        if not election.external_identifier:
            raise ValueError('At least one external identifier is required for an Election.')
        # require the election scope id to reference a valid reporting unit
        app_state.reporting_units.by_ref(election.election_scope_id)

    @router.post('/elections')
    @request_handler
    def create_election(req: ApiRequest[Election]) -> str:
        _validate_election(req.data)
        return app_state.elections.put(req.data, overwrite=False)

    @router.get('/elections')
    @request_handler
    def get_elections() -> List[Election]:
        return list(app_state.elections.values())

    @router.get('/elections/{election_id}')
    @request_handler
    def get_election(election_id: str) -> Election:
        return app_state.elections.get(election_id)

    @router.put('/elections/{election_id}')
    @request_handler
    def update_election(election_id: str, req: ApiRequest[Election]) -> str:
        # check that the record exists before updating
        app_state.elections.get(election_id)
        _validate_election(req.data)
        return app_state.elections.put(req.data, overwrite=True)

    @router.delete('/elections/{election_id}')
    @request_handler
    def delete_election(election_id: str) -> bool:
        return app_state.elections.delete(election_id)

    return router
