from fastapi import FastAPI
import uvicorn
import loguru


class Server:
    def __init__(self) -> None:
        self.app = FastAPI()

    def run(self):
        uvicorn.run(self.app)