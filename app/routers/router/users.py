from fastapi import APIRouter
from app.routers.controllers.user.create import create_user


router = APIRouter(prefix='/user', tags=['users'])

router.post('/create')(create_user)

