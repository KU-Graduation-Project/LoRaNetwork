from kafka import KafkaProducer
from json import dumps
import time

producer = KafkaProducer(acks=0, compression_type='gzip',
                         bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

start = time.time()
for i in range(1000):
    data = {'str': 'result' + str(i)}
    producer.send('test', value=data)
    producer.flush()
print("elapsed :", time.time() - start)
