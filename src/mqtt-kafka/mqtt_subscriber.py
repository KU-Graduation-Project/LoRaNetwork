import paho.mqtt.client as mqtt
import time

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTConsumer')
mqtt_client.connect(mqtt_broker_address)


def on_message(client, userdata, message):
    msg_payload = str(message.payload)
    print('Received MQTT message', msg_payload)


mqtt_client.loop_start()
mqtt_client.subscribe('new-topic') #토픽 지정
mqtt_client.on_message = on_message
time.sleep(300)
mqtt_client.loop_stop()
