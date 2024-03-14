from fastapi import APIRouter
from app.routers.controllers.finger.create import scan_finger

router = APIRouter(prefix='/finger', tags=['fingers'])

router.post('/create')(scan_finger)
