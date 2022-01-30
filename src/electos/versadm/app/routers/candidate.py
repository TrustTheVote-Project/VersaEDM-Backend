from typing import List, Set, Union

from fastapi import APIRouter

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.candidate import Candidate
from versadm.models.nist.classes.contest import CandidateContest, RetentionContest
from versadm.models.nist.classes.contest_selection import CandidateSelection
from versadm.models.nist.classes.election import Election
from versadm.models.nist.enums.type_tag import TypeTags


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    def _get_candidate_contest(election: Election, contest_id: str) -> Union[CandidateContest, RetentionContest]:
        contest = app_state.contests.get(contest_id)
        if contest not in election.contest:
            raise ValueError(f'Contest {contest_id} does not belong to the specified election.')
        if contest.obj_type not in (TypeTags.CandidateContestTag, TypeTags.RetentionContestTag):
            raise ValueError(f'Unexpected contest type {contest.obj_type}; must be candidate or retention contest.')
        return contest

    def _candidate_obj_refs(contest: Union[CandidateContest, RetentionContest]) -> Set[str]:
        if contest.obj_type == TypeTags.CandidateContestTag:
            return {cand_id.value() for c_sel in contest.contest_selection for cand_id in c_sel.candidate_ids}
        elif contest.obj_type == TypeTags.RetentionContestTag:
            return {contest.candidate_id.value()}
        else:
            return set()

    @router.post('/elections/{election_id}/contests/{contest_id}/candidates')
    @request_handler
    def create_candidate(election_id: str, contest_id: str, req: ApiRequest[Candidate]) -> str:
        # verify the election is legit
        election: Election = app_state.elections.get(election_id)
        # verify the contest is legit
        contest = _get_candidate_contest(election, contest_id)
        candidate = app_state.candidates.put(req.data, overwrite=False)
        # Add the candidate to the election
        election.candidate.append(candidate)
        app_state.elections.put(election, overwrite=True)
        # Add the candidate to the contest
        candidate_selection = CandidateSelection(
            candidate_ids=[candidate.obj_id],
        )
        contest.contest_selection.append(candidate_selection)
        app_state.contests.put(contest, overwrite=True)
        return candidate

    @router.get('/elections/{election_id}/contests/{contest_id}/candidates')
    @request_handler
    def get_candidates(election_id: str, contest_id: str) -> List[Candidate]:
        election = app_state.elections.get(election_id)
        contest = _get_candidate_contest(election, contest_id)
        contest_candidate_ids = _candidate_obj_refs(contest)
        return [candidate for candidate in app_state.candidates.values() if candidate.obj_id in contest_candidate_ids]

    @router.get('/elections/{election_id}/candidates/{candidate_id}')
    @request_handler
    def get_candidate(election_id: str, candidate_id: str) -> Candidate:
        election = app_state.elections.get(election_id)
        return app_state.candidates.get(candidate_id)

    @router.put('/candidates/{candidate_id}')
    @request_handler
    def update_candidate(candidate_id: str, req: ApiRequest[Candidate]) -> str:
        # check that the record exists before updating
        app_state.candidates.get(candidate_id)
        return app_state.candidates.put(req.data, overwrite=True)

    @router.delete('/candidates/{candidate_id}')
    @request_handler
    def delete_candidate(candidate_id: str) -> bool:
        candidate = app_state.candidates.get(candidate_id)
        for election_id, election in app_state.elections.items():
            for contest in [c for c in election.contest if candidate.obj_id.value() in _candidate_obj_refs(c)]:
                if contest.obj_type == TypeTags.CandidateContestTag:
                    # A candidate contest references multiple candidates and can exist independently.
                    for c_sel in contest.contest_selection:
                        c_sel.candidate_ids.remove(candidate.obj_id)
                    app_state.contests.put(contest, overwrite=True)
                elif contest.obj_type == TypeTags.RetentionContestTag:
                    # The retention contest cannot exist independent of the candidate, so remove it too.
                    app_state.contests.delete(contest.obj_id)
            election.candidate.remove(candidate)
            app_state.elections.put(election, overwrite=True)

        return app_state.candidates.delete(candidate_id)

    return router
