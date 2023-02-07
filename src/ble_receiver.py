import asyncio
from bleak import BleakClient

#scan시 arduino라는 이름으로 인식될 수 있음
address = "E69FDBAC-4750-BF6F-0C68-5646E82D36E3"

read_write_charcteristic_uuid = "0000FFF1-0000-1000-8000-00805F9B34FB"


async def run(address):
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()
        # 서비스내에 있는 캐릭터리스틱 정보 보기
        for service in services:
            print(service)
            print('\tuuid:', service.uuid)
            print('\tcharacteristic list:')
            for characteristic in service.characteristics:
                print('\t\t', characteristic)
                print('\t\tuuid:', characteristic.uuid)
                print('\t\tdescription :', characteristic.description)
                # ['write-without-response', 'write', 'read', 'notify']
                print('\t\tproperties :', characteristic.properties)

        # 읽기/쓰기 캐릭터리스틱 uuid를 이용해 데이터 읽기
        # 해당 캐릭터리스틱의 속성에는 read가 존재해야만 읽기가 가능하다.
        read_data = await client.read_gatt_char(read_write_charcteristic_uuid)
        # 읽근 데이터 출력
        print('read_data: ', read_data)

    print('disconnect')


loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')




