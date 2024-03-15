from fastapi import HTTPException, BackgroundTasks
from app.services.db import check_db
from pyzkfp import ZKFP2
from app.routers.controllers.finger.scan import scan_finger
import json

async def create_worker_finger(user_id: int):
    zkfp2 = ZKFP2()
    zkfp2.Init()

    user_db = check_db.fetch_one(
        sql="SELECT * FROM users WHERE id = %s",
        params=(user_id,)
    )

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    finger_user_db = check_db.fetch_one(
        sql="SELECT * FROM fingerprints WHERE user_id = %s",
        params=(user_id,)
    )
    if finger_user_db and finger_user_db['fingerprint']:
        raise HTTPException(status_code=400, detail="User already has fingerprints")

    res = await scan_finger()

    res['tmp'] = bytearray(res['tmp'])

    save_finger = check_db.execute(
        sql = "INSERT INTO fingerprints (user_id, fingerprint, tmp) VALUES (%s, %s, %s)",
        params = (
            user_id,
            res['fingerprints'],
            res['tmp']
        )
    )
    if not save_finger:
        raise HTTPException(status_code=500, detail="Error saving fingerprints")
    import bcrypt
    finger_user_db = check_db.fetch_one(
        sql="SELECT * FROM fingerprints WHERE user_id = %s",
        params=(user_id,)
    )

    bcrypt_finger = bcrypt.hashpw(finger_user_db['fingerprint'].encode('utf-8'), bcrypt.gensalt())

    return {
        'status': 'success',
        'message': 'Fingerprints registered successfully',
        'user': user_db,
        #'fingerprint_cryp': bcrypt_finger.decode('utf-8'),
        'fingerprint': finger_user_db['fingerprint']
    }


