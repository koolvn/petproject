import json
import numpy as np
import base64
import time

from kafka import KafkaProducer


# ### Numpy as is
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092',
                         client_id='Test write',
                         buffer_memory=1e9,  # bytes
                         max_request_size=1e9,  # bytes
                         value_serializer=lambda v: json.dumps(v).encode('utf-8')
                         )

print(producer.config)
topic = 'tg_requests'
img = np.ones((1080 // 2, 1920 // 2, 3), dtype=np.uint8)
img_numpy = json.dumps({'image_numpy': img}, cls=NumpyEncoder)

for i in range(3):
    t0 = time.time()
    print(f'Sending message #{i}')
    data = {'user': f'{time.time()}',
            'request': {'text': 'Hello world',
                        'media': img_numpy}
            }
    producer.send(topic, value=data, key=bytes(str(time.time()), 'utf-8')).get(timeout=10) # , partition=0)
    print(f'Took {time.time() - t0:.1f} sec.')
producer.close()
#
# ### bytes topic
# topic = 'tg_bytes'
# producer = KafkaProducer(bootstrap_servers='localhost:9092',
#                          client_id='Test write',
#                          buffer_memory=1e9,  # bytes
#                          max_request_size=1e9,  # bytes
#                          )
#
# print(producer.DEFAULT_CONFIG)
#
# img_bytes = np.ones((1080, 1920, 3), dtype=np.uint8).tobytes()
# print(f'{img_bytes.__sizeof__() / 1024 / 1024:.2f} Mb')
# # img_bytes = base64.b64encode(img_bytes)
# # print(f"{bytes(img_bytes.decode('utf-8'), 'utf-8').__sizeof__() / 1024 / 1024:.2f} Mb")
#
#
# for i in range(3):
#     print(f'Sending message #{i}')
#     producer.send(topic, value=img_bytes, key=bytes(str(time.time()), 'utf-8'))
#
# producer.close()
