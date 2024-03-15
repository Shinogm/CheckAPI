from pyzkfp import ZKFP2
from fastapi import HTTPException, BackgroundTasks
from app.services.db import check_db
import asyncio

async def scan_finger(range_int: int | None = None):
    zkfp2 = ZKFP2()
    zkfp2.Init()

    device_count = zkfp2.GetDeviceCount()
    print(f"{device_count} devices found")
    zkfp2.OpenDevice(0)
    blob_image = None

    tmps = []

    for i in range(range_int if range_int else 3):
        while True:
            zkfp2.Light('green', duration=10)

            try:
                capture = zkfp2.AcquireFingerprint()
                if capture:
                    print('fingerprint captured')
                    tmp, img = capture
                    tmps.append(tmp)
                    blob_image =    zkfp2.Blob2Base64String(img)

                    await asyncio.sleep(0.5)
                    break
            except Exception as e:
                print(e)
                await asyncio.sleep(0.5)

    regTemp, regTempLe = zkfp2.DBMerge(*tmps)

    zkfp2.CloseDevice()

    return {
        'status': 'success',
        'message': 'Fingerprints registered successfully',
        'fingerprints': blob_image,
        'tmp': regTemp
    }



'''
async def main():
    res = await scan_finger()

if __name__ == '__main__':
    asyncio.run(main())
'''


