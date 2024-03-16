from fastapi import APIRouter
from app.routers.controllers.perms import get

router = APIRouter(prefix='/perms', tags=['permission'])

router.get('/get')(get.get_perms)
