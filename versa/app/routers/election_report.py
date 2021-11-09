from fastapi import APIRouter

from versa.app.db.in_memory import InMemoryDb


def create_router(app_state: InMemoryDb):

    router = APIRouter()

    return router
