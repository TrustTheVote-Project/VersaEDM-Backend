from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    # TODO: define methods

    @app.head('/health')
    def health_check():
        return True

    return app
