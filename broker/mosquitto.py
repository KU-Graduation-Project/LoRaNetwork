# publisher
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    # 연결이 성공적으로 된다면 완료 메세지 출력
    if rc == 0:
        print("completely connected")
    else:
        print("Bad connection Returned code=", rc)


# 연결이 끊기면 출력
def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)


mqttc = mqtt.Client("client1")
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect("127.0.0.1", 1883)
mqttc.publish("client1/gsensor", "this is message from mqtt producer")
