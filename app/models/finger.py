from pydantic import BaseModel
from typing import Annotated

class Finger(BaseModel):
    fingerprint: str
    blob: Annotated[bytes,[3]]

