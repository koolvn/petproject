import base64
import json
import io
import numpy as np
from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord
from PIL import Image


TOPIC = 'tg_requests'  # 'tg_bytes'  # 'input'  #
OFFSET1 = 0  # 14
OFFSET2 = 0  # 19


def parse_media(media: dict):
    results = []
    if not isinstance(media, dict):
        media = json.loads(media) if isinstance(media, (bytes, str)) else {}
    for key in media.keys():
        print(key)
        if key == 'image_b64':
            res = base64.decodebytes(media['image_b64'].encode('utf-8'))
            res = Image.open(io.BytesIO(res))
            results.append(res)
        if key == 'image_numpy':
            res = json.loads(v['request']['media']).get('image_numpy')
            results.append(res)
    if len(results) > 0:
        return results[-1]
    else:
        return None


consumer = KafkaConsumer(bootstrap_servers='127.0.0.1:9092',
                         group_id='test_group',
                         enable_auto_commit=False, auto_offset_reset='latest',
                         fetch_max_bytes=int(1e9), max_partition_fetch_bytes=int(1e9),
                         receive_buffer_bytes=int(1e9))
cnt = 0
print(consumer.config)
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

    user = v['user']
    text = v['request']['text']
    print(f'User {user} sent text {text}')
    image = parse_media(v['request']['media'])

    if image is not None:
        image = np.asarray(image)
        print(f'User {user} sent an image {image.shape = }')

    consumer.commit()

consumer.close()
