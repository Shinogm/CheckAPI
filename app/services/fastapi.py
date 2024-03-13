from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from app.models.static_dir import StaticDir
from fastapi.middleware.cors import CORSMiddleware

class App():
    def __init__(
        self,
        routers: list[APIRouter] = [],
        static_dirs: list[StaticDir] = []
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

        for static_dir in static_dirs:
            self._add_static_dir(static_dir)
        pass

    def _add_router(self, router: APIRouter) -> None:
        self.app.include_router(router)

    def _add_static_dir(self, static_dir: StaticDir) -> None:
        self.app.mount(f'/{static_dir.name}', StaticFiles(directory=static_dir.path), name=static_dir.name)

    def get_app(self) -> FastAPI:
        return self.app