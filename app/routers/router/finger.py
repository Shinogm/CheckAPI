from fastapi import APIRouter
from app.routers.controllers.finger import scan, create, get

router = APIRouter(prefix='/finger', tags=['fingers'])

router.post('/create')(scan.scan_finger)
router.post('/create/worker')(create.create_worker_finger)

router.get('/get/{user_id}')(get.get_finger_image)