import asyncio
import time
from datetime import datetime

from bleak import BleakClient

#scan시 arduino라는 이름으로 인식될 수 있음
address = "E69FDBAC-4750-BF6F-0C68-5646E82D36E3"

#0000(****)-0000 부분의 UUID만 설정하면 됨(16bit->128bit 변환)
accelerometerCharacteristic_X_uuid = "0000FFA1-0000-1000-8000-00805F9B34FB"


async def run(address):
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()

        for service in services:
            print("service:", service)
            # print('\tuuid:', service.uuid)
            # print('\tcharacteristic list:')

            while True:
                time.sleep(1)
                now = datetime.now()
                timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                print(' ', timestamp)
                for characteristic in service.characteristics:
                    # print('\t', characteristic)
                    print('\t', characteristic.uuid)
                    # print('\t\tdescription :', characteristic.description)
                    # ['write-without-response', 'write', 'read', 'notify']
                    # print('\t\tproperties :', characteristic.properties)

                    # characteristic uuid로 데이터 읽기(characteristic 속성에 read가 존재해야 가능)
                    data = int.from_bytes(await client.read_gatt_char(characteristic.uuid), byteorder='little', signed=True)
                    print('\t data: ', data)

    print('disconnect')


loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')




