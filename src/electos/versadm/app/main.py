from fastapi import FastAPI
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.requests import Request
from starlette.responses import JSONResponse

from versadm.app.db.in_memory import InMemoryDb
from versadm.app import routers
from versadm.app.util.errors import ReferentialIntegrityError, DuplicateObjectError


def create_app(app_state=InMemoryDb()) -> FastAPI:
    app = FastAPI()

    @app.exception_handler(ReferentialIntegrityError)
    def handle_ref_error(_: Request, exc: ReferentialIntegrityError):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={'type': exc.error_code, 'msg': exc.args[0]}
        )

    @app.exception_handler(DuplicateObjectError)
    def handle_duplicate_object_error(_: Request, exc: DuplicateObjectError):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={'type': exc.error_code, 'msg': exc.args[0]}
        )

    app.include_router(routers.ballot_style.create_router(app_state))
    app.include_router(routers.candidate.create_router(app_state))
    app.include_router(routers.contest.create_router(app_state))
    app.include_router(routers.election.create_router(app_state))
    app.include_router(routers.election_report.create_router(app_state))
    app.include_router(routers.header.create_router(app_state))
    app.include_router(routers.health.router)
    app.include_router(routers.office.create_router(app_state))
    app.include_router(routers.party.create_router(app_state))
    app.include_router(routers.person.create_router(app_state))
    app.include_router(routers.reporting_unit.create_router(app_state))

    return app
