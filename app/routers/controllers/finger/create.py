from fastapi import HTTPException, BackgroundTasks
from app.services.db import check_db
from app.routers.controllers.finger.scan import scan_finger

async def create_worker_finger(user_id: int):

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

    save_finger = check_db.execute(
        sql = "INSERT INTO fingerprints (user_id, fingerprint) VALUES (%s, %s)",
        params = (
            user_id,
            res['fingerprints']
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


