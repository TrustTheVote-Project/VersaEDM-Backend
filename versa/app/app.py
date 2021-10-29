from fastapi import FastAPI

from .db.in_memory import InMemoryDb
from .routers import health, party


def create_app() -> FastAPI:
    app = FastAPI()
    app_state = InMemoryDb()

    app.include_router(health.router)
    app.include_router(party.create_router(app_state))

    return app
