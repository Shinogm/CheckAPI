from pydantic import BaseModel
from fastapi import Form
from typing import Annotated
class User(BaseModel):
    name: str
    domicilio: str
    telefono: str
    empresa: str
    email: str
    password: str | None = None

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form(...)],
        domicilio: Annotated[str, Form(...)],
        telefono: Annotated[str, Form(...)],
        empresa: Annotated[str, Form(...)],
        email: Annotated[str, Form(...)],
        password: Annotated[str | None, Form(...)] = None,
    ):
        return cls(
            name=name,
            domicilio=domicilio,
            telefono=telefono,
            empresa=empresa,
            email=email,
            password=password,
        )
        
