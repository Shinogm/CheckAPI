from fastapi import APIRouter
from app.routers.controllers.user import create, get, identify, modify, delete
from app.utils import login

router = APIRouter(prefix='/user', tags=['users'])

router.post('/create')(create.create_user)
router.post('/user/login')(login.verify_password)
router.post('/user/identify')(identify.indentity)

router.get('/get')(get.get_all_users)
router.get('/get/permissions/{perrm_id}')(get.get_all_user_by_perm_id)
router.get('/get/horario')(get.get_horario_by_scan)

router.put('/modify/{user_id}')(modify.modify_user)

router.delete('/delete/{user_id}')(delete.delete_user)
