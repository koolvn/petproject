import json

import numpy as np
from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord
TOPIC = 'tg_requests111'  # 'tg_bytes'  #
OFFSET1 = 14
OFFSET2 = 19

consumer = KafkaConsumer(bootstrap_servers='localhost:9092',  group_id='test_group',
                         enable_auto_commit=False, auto_offset_reset='latest',
                         fetch_max_bytes=int(1e9), max_partition_fetch_bytes=int(1e9),
                         receive_buffer_bytes=int(1e9))
cnt = 0
print(consumer.config)
# topic_partition = TopicPartition(TOPIC, 0)
# print(topic_partition)
partitions = [TopicPartition(TOPIC, x) for x in range(2)]
consumer.assign(partitions)
consumer.seek(TopicPartition(TOPIC, 0), OFFSET1)
consumer.seek(TopicPartition(TOPIC, 1), OFFSET2)
# consumer.seek_to_beginning(*partitions)
for msg in consumer:
    cnt += 1
    print(f'Message # {cnt}.  {msg.partition = }  {msg.offset = }')

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
    consumer.commit()

consumer.close()
