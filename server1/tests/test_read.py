import base64
import json
import io
import logging

import numpy as np
from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord
from PIL import Image

KAFKA_IP = '127.0.0.1'
KAFKA_PORT = 9092
GROUP_ID = 'test_group'
TOPIC = 'tg_requests'  # 'tg_bytes'  # 'input'  #
NUM_PARTITIONS = 2
OFFSETS = [0, 3]
FROM_BEGINNING = False

assert len(OFFSETS) == NUM_PARTITIONS


def parse_media(media: dict):
    results = []
    if not isinstance(media, dict):
        media = json.loads(media) if isinstance(media, (bytes, str)) else {}
    for key, value in media.items():
        print(key)
        res = media[key]
        if key == 'image_b64':
            res = base64.decodebytes(value.encode('utf-8'))
            res = Image.open(io.BytesIO(res))
        elif key == 'image_numpy':
            res = json.loads(value)
        else:
            logging.warning(f'Media Type = {key} not implemented. Passing as is')
        results.append(res)

    if len(results) > 0:
        return results[-1]
    else:
        return None


if __name__ == '__main__':
    consumer = KafkaConsumer(bootstrap_servers=f'{KAFKA_IP}:{KAFKA_PORT}',
                             group_id=GROUP_ID,
                             enable_auto_commit=False, auto_offset_reset='latest',
                             fetch_max_bytes=int(1e9), max_partition_fetch_bytes=int(1e9),
                             receive_buffer_bytes=int(1e9))
    cnt = 0
    print(consumer.config)
    partitions = [TopicPartition(TOPIC, x) for x in range(NUM_PARTITIONS)]
    consumer.assign(partitions)
    if FROM_BEGINNING:
        consumer.seek_to_beginning(*partitions)
    else:
        [consumer.seek(TopicPartition(TOPIC, part_), offset)
         for part_, offset in zip(range(NUM_PARTITIONS), OFFSETS)]

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
