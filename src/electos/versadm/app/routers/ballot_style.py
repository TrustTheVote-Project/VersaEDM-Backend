from typing import List

from fastapi import APIRouter

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.ballot_style import BallotStyle
from versadm.models.nist.classes.election import Election


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    @router.post('/elections/{election_id}/ballot-styles')
    @request_handler
    def create_ballot_style(election_id: str, req: ApiRequest[BallotStyle]) -> str:
        # verify the election is legit
        election: Election = app_state.elections.get(election_id)
        ballot_style = app_state.ballot_styles.put(req.data, overwrite=False)
        # Add the ballot style to the election
        election.ballot_style.append(ballot_style)
        app_state.elections.put(election, overwrite=True)
        return ballot_style

    @router.get('/elections/{election_id}/ballot-styles')
    @request_handler
    def get_ballot_styles(election_id: str) -> List[BallotStyle]:
        election = app_state.elections.get(election_id)
        return election.ballot_style

    @router.get('/elections/{election_id}/ballot-styles/{ballot_style_id}')
    @request_handler
    def get_candidate(election_id: str, ballot_style_id: str) -> BallotStyle:
        election = app_state.elections.get(election_id)
        return app_state.ballot_styles.get(ballot_style_id)

    @router.put('/elections/{election_id}/ballot-styles/{ballot_style_id}')
    @request_handler
    def update_ballot_style(election_id: str, ballot_style_id: str, req: ApiRequest[BallotStyle]) -> str:
        # check that the record exists before updating
        election = app_state.elections.get(election_id)
        # TODO: make sure ballot style belongs to the election
        app_state.ballot_styles.get(ballot_style_id)
        return app_state.ballot_styles.put(req.data, overwrite=True)

    @router.delete('/elections/{election_id}/ballot-styles/{ballot_style_id}')
    @request_handler
    def delete_ballot_style(ballot_style_id: str) -> bool:
        ballot_style = app_state.ballot_styles.get(ballot_style_id)
        for election_id, election in app_state.elections.items():
            election.ballot_style.remove(ballot_style)
            app_state.elections.put(election, overwrite=True)

        return app_state.ballot_styles.delete(ballot_style_id)

    return router
