import json

import numpy as np
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

TOPIC = 'tg_requests'  # 'tg_bytes'  #

consumer = KafkaConsumer(TOPIC, bootstrap_servers='localhost:9092',
                         fetch_max_bytes=int(1e9), max_partition_fetch_bytes=int(1e9),
                         receive_buffer_bytes=int(1e9))
cnt = 0
print(consumer.config)
for msg in consumer:
    cnt += 1
    print(cnt)

    k = json.loads(msg.key)
    v = json.loads(msg.value)

    user = float(v['user'])
    text = v['request']['text']
    print(f'User {user} sent text {text}')
    image = json.loads(v['request']['media']).get('image')
    if image is not None:
        image = np.asarray(image)
        print(f'User {user} sent an image {image.shape = }')
    # print(v['request'].keys())
    # print(k, user, f'{len(image.tobytes()) / 1024 / 1024:.3f} Mb')

consumer.close()
