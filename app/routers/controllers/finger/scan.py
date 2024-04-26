from pyzkfp import ZKFP2
from fastapi import HTTPException, BackgroundTasks
import asyncio

async def scan_finger(background_tasks: BackgroundTasks):
    zkfp2 = ZKFP2()
    zkfp2.Init()

    device_count = zkfp2.GetDeviceCount()
    print(f"{device_count} devices found")
    zkfp2.OpenDevice(0)
    blob_image = None

    tmps = []

    for i in range(3):
        while True:
            zkfp2.Light('green', duration=10)

            try:
                capture = zkfp2.AcquireFingerprint()
                if capture:
                    print('fingerprint captured')
                    tmp, img = capture
                    if not tmps or zkfp2.DBMatch(tmps[-1], tmp) > 0:
                        tmps.append(tmp)
                        blob_image = zkfp2.Blob2Base64String(img)
                    else:
                        print('Different finger. Please enter the original finger!')
                        zkfp2.Light('red', duration=1)
                        background_tasks.add_task(handle_failed_capture)
                        continue

                    await asyncio.sleep(0.5)
                    break
            except Exception as e:
                print(e)
                raise HTTPException(status_code=500, detail='Error capturing fingerprint')

    regTemp, regTempLe = zkfp2.DBMerge(*tmps)

    zkfp2.CloseDevice()

    return {
        'status': 'success',
        'message': 'Fingerprints registered successfully',
        'fingerprints': blob_image,
        'tmp': regTemp
    }

def handle_failed_capture():
    # Tarea a ejecutar cuando la captura del dedo falla
    print('Fingerprint capture failed')
    # Agregar aquí cualquier lógica adicional que necesites para manejar la falla de la captura del dedo



'''
async def main():
    res = await scan_finger()

if __name__ == '__main__':
    asyncio.run(main())

'''
