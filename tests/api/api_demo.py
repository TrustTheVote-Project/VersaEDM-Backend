"""
Can we get an API endpoint up and running with our dev config?
"""
from fastapi import FastAPI
import uvicorn

# from versa.app import create_app
# import versa.app

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
