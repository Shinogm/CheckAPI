from pyzkfp import ZKFP2
from fastapi import HTTPException, BackgroundTasks
from app.services.db import check_db
import logging
from time import sleep
from threading import Thread
import asyncio

async def scan_finger(range_int: int | None = None):
    zkfp2 = ZKFP2()
    zkfp2.Init()
    device_count = zkfp2.GetDeviceCount()
    print(f"{device_count} devices found")
    zkfp2.OpenDevice(0)
    blob_image = None
    for i in range(range_int or 3):
        while True:
            zkfp2.Light('green', duration=10)
            capture = zkfp2.AcquireFingerprint()
            if capture:
                print('fingerprint captured')
                tmp, img = capture
                blob_image = zkfp2.Blob2Base64String(img)

                await asyncio.sleep(0.5)
                break
    return {
        'status': 'success',
        'message': 'Fingerprints registered successfully',
        'fingerprints': blob_image
    }



'''
async def main():
    res = await scan_finger()

if __name__ == '__main__':
    asyncio.run(main())
'''


