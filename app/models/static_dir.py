from pydantic import BaseModel

class StaticDir(BaseModel):
    name: str
    path: str