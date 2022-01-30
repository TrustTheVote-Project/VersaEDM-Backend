from typing import List, Union

from fastapi import APIRouter

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.contest import BallotMeasureContest, CandidateContest


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    def _validate_contest(contest: Union[BallotMeasureContest, CandidateContest]):
        # the election district ID must reference an existing reporting unit
        app_state.reporting_units.by_ref(contest.election_district_id)

    @router.post('/elections/{election_id}/contests')
    @request_handler
    def create_contest(election_id: str, req: ApiRequest[Union[BallotMeasureContest, CandidateContest]]) -> str:
        # verify the election is legit
        election = app_state.elections.get(election_id)
        _validate_contest(req.data)
        contest_id = app_state.contests.put(req.data, overwrite=False) or req.data.obj_id
        # Add the contest to the election
        election.contest.append(app_state.contests.get(contest_id))
        app_state.elections.put(election, overwrite=True)
        return contest_id

    @router.get('/elections/{election_id}/contests')
    @request_handler
    def get_contests(election_id: str) -> List[Union[BallotMeasureContest, CandidateContest]]:
        election = app_state.elections.get(election_id)
        return [contest for contest in app_state.contests.values() if contest in election.contest]

    @router.get('/contests/{contest_id}')
    @request_handler
    def get_contest(contest_id: str) -> Union[BallotMeasureContest, CandidateContest]:
        return app_state.contests.get(contest_id)

    @router.put('/contests/{contest_id}')
    @request_handler
    def update_contest(contest_id: str, req: ApiRequest[Union[BallotMeasureContest, CandidateContest]]) -> str:
        # check that the record exists before updating
        existing_record = app_state.contests.get(contest_id)
        # don't allow changing the type of contest
        if existing_record.obj_type != req.data.obj_type:
            raise ValueError(f'Contest cannot be updated to a different type')
        _validate_contest(req.data)
        return app_state.contests.put(req.data, overwrite=True)

    @router.delete('/contests/{contest_id}')
    @request_handler
    def delete_contest(contest_id: str) -> bool:
        contest = app_state.contests.get(contest_id)
        for election_id, election in app_state.elections.items():
            election.contest.remove(contest)
            app_state.elections.put(election, overwrite=True)
        return app_state.contests.delete(contest_id)

    return router
