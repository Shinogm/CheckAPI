from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

class App():
    def __init__(
        self,
        routers: list[APIRouter] = [],
    ) -> None:
        self.app = FastAPI()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )

        for router in routers:
            self._add_router(router)

        
        pass

    def _add_router(self, router: APIRouter) -> None:
        self.app.include_router(router)

    def get_app(self) -> FastAPI:
        return self.app