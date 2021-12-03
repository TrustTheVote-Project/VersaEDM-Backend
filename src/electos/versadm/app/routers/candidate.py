from typing import List, Set

from fastapi import APIRouter

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.candidate import Candidate
from versadm.models.nist.classes.contest import CandidateContest
from versadm.models.nist.classes.contest_selection import CandidateSelection
from versadm.models.nist.enums.type_tag import TypeTags


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    def _get_candidate_contest(contest_id) -> CandidateContest:
        contest = app_state.contests.get(contest_id)
        if contest.obj_type != TypeTags.CandidateContestTag:
            raise ValueError(f'Expected object of type {TypeTags.CandidateContestTag} but got {contest.obj_type}')
        return contest

    def _candidate_obj_refs(contest: CandidateContest) -> Set[str]:
        return {cand_id for c_sel in contest.contest_selection for cand_id in c_sel.candidate_ids}

    @router.post('/contests/{contest_id}/candidates')
    @request_handler
    def create_candidate(contest_id: str, req: ApiRequest[Candidate]) -> str:
        # verify the contest is legit
        contest = _get_candidate_contest(contest_id)
        candidate = app_state.candidates.put(req.data, overwrite=False)
        # Add the candidate to the contest
        candidate_selection = CandidateSelection(
            candidate_ids=[candidate.obj_id],
        )
        contest.contest_selection.append(candidate_selection)
        app_state.contests.put(contest, overwrite=True)
        return candidate

    @router.get('/contests/{contest_id}/candidates')
    @request_handler
    def get_candidates(contest_id: str) -> List[Candidate]:
        contest = _get_candidate_contest(contest_id)
        contest_candidate_ids = _candidate_obj_refs(contest)
        return [candidate for candidate in app_state.candidates.values() if candidate.obj_id in contest_candidate_ids]

    @router.get('/candidates/{candidate_id}')
    @request_handler
    def get_candidate(candidate_id: str) -> Candidate:
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
        contests = [contest for contest in app_state.contests.values()
                    if candidate.obj_id in _candidate_obj_refs(contest)]
        for contest in contests:
            for c_sel in contest.contest_selection:
                c_sel.candidate_ids.remove(candidate.obj_id)
            app_state.contests.put(contest, overwrite=True)
        return app_state.candidates.delete(candidate_id)

    return router
