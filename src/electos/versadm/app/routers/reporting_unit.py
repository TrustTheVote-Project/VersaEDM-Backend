from typing import List

from fastapi import APIRouter

from versadm.api.api_request import ApiRequest
from versadm.app.db.in_memory import InMemoryDb
from versadm.app.routers.common import create_api_decorator
from versadm.models.nist.classes.gp_unit import ReportingUnit


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    request_handler = create_api_decorator(app_state)

    @router.post('/reporting_units')
    @request_handler
    def create_reporting_unit(req: ApiRequest[ReportingUnit]) -> str:
        return app_state.reporting_units.put(req.data, overwrite=False)

    @router.get('/reporting_units')
    @request_handler
    def get_reporting_units() -> List[ReportingUnit]:
        return app_state.reporting_units.values()

    @router.put('/reporting_units/{reporting_unit_id}')
    @request_handler
    def update_reporting_unit(reporting_unit_id: str, req: ApiRequest[ReportingUnit]) -> str:
        # check that the record exists before updating
        app_state.reporting_units.get(reporting_unit_id)
        return app_state.reporting_units.put(req.data, overwrite=True)

    @router.delete('/reporting_units/{reporting_unit_id}')
    @request_handler
    def delete_reporting_unit(reporting_unit_id: str) -> bool:
        return app_state.reporting_units.delete(reporting_unit_id)

    return router
