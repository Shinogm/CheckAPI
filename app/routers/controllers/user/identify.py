from app.routers.controllers.finger.scan import scan_finger
from pyzkfp import ZKFP2
from app.services.db import check_db
import json

async def indentity(range: int = 3):
    zkfp2 = ZKFP2()
    zkfp2.Init()
    zkfp2.DBInit()
    zkfp2.DBClear()

    scan = await scan_finger(range)

    fingerprints = check_db.fetch_all(
        sql="SELECT id, tmp FROM fingerprints",
    )

    for fingerprint in fingerprints:
        zkfp2.DBAdd(fingerprint['id'], bytes(fingerprint['tmp']))

    fingerprint_id, score = zkfp2.DBIdentify(scan['tmp'])

    print(fingerprint_id, score)

    if fingerprint_id == 0 or score < 60:
        raise Exception('Fingerprint not found')
    
    user = check_db.fetch_one(
        sql='''
            SELECT 
                user.*
            FROM fingerprints
            JOIN users user ON user.id = fingerprints.user_id
            WHERE fingerprints.id = %s
        ''',
        params=(fingerprint_id,)
    )


    return {
        'status': 'success',
        'score': score,
        'user': user,
    }
