from fastapi import APIRouter

from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.election_report import ElectionReport
from versadm.models.nist.enums.type_tag import TypeTags


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    @router.put('/admin/load_election_data')
    @request_handler
    def load_election_data(election_data: ElectionReport):
        for party in election_data.party:
            app_state.parties.put(party, overwrite=True)
        for person in election_data.person:
            app_state.persons.put(person, overwrite=True)
        for gp_unit in election_data.gp_unit:
            if gp_unit.obj_type == TypeTags.ReportingUnitTag:
                app_state.reporting_units.put(gp_unit, overwrite=True)
        for office in election_data.office:
            app_state.offices.put(office, overwrite=True)
        for election in election_data.election:
            for candidate in election.candidate:
                app_state.candidates.put(candidate, overwrite=True)
            for contest in election.contest:
                app_state.contests.put(contest, overwrite=True)
            app_state.elections.put(election, overwrite=True)
        return True

    return router
