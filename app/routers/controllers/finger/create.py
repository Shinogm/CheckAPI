from pyzkfp import ZKFP2
from fastapi import HTTPException, BackgroundTasks
from app.services.db import check_db
import logging
from time import sleep
from threading import Thread
import asyncio

async def scan_finger(user_id: int | None = None):
    zkfp2 = ZKFP2()
    zkfp2.Init()
    device_count = zkfp2.GetDeviceCount()
    print(f"{device_count} devices found")
    zkfp2.OpenDevice(0)
    templates = []
    for i in range(3):
        while True:
            capture = zkfp2.AcquireFingerprint()
            if capture:
                print('fingerprint captured')
                tmp, img = capture
                blob_image = zkfp2.Blob2Base64String(img)
                db_img = check_db.fetch_one(
                    sql='SELECT * FROM fingerprints WHERE fingerprint = %s',
                    params=(blob_image,)
                )
                if db_img is not None:
                    bytes_img = zkfp2.Base64String2Blob(db_img["fingerprint"])
                    res = zkfp2.DBMatch(img, bytes_img)

                    if res:
                        print('Fingerprint already registered')
                        break

                if user_id is not None:
                    templates.append(tmp)
                    db_insert = check_db.insert(
                        table='fingerprints',
                        data={
                            'fingerprint': blob_image,
                            'user_id': user_id
                        }
                    )
                    await asyncio.sleep(3)
                    return {
                        'status': 'success',
                        'message': 'Fingerprints registered successfully',
                        'fingerprints': blob_image
                    }
                break
    fingerprint_id, score = zkfp2.DBIdentify(tmp)
    print(fingerprint_id, score)



'''
async def main():
    res = await scan_finger()

if __name__ == '__main__':
    asyncio.run(main())
'''


