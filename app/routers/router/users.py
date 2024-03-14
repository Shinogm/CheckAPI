from fastapi import APIRouter
from app.routers.controllers.user.create import create_user
from app.utils import login

router = APIRouter(prefix='/user', tags=['users'])

router.post('/create')(create_user)
router.post('/user/login')(login.verify_password)


