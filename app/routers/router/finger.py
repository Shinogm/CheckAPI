from fastapi import APIRouter
from app.routers.controllers.finger import scan, create

router = APIRouter(prefix='/finger', tags=['fingers'])

router.post('/create')(scan.scan_finger)
router.post('/create/worker')(create.create_worker_finger)
