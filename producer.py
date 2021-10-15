import os
import json
import random

from google.cloud import pubsub_v1
from time import sleep

private_key_path = 'PATH_TO_YOUR_PRIVATE_KEY'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key_path

publisher = pubsub_v1.PublisherClient()
topic_path = 'YOUR_PUBLICATION_PATH_FOR_CLASSIFYME_TOPIC'

string_stream_list = json.load(open('data/StringStream.json', 'r'))

for idx, string in enumerate(string_stream_list):
    data = f'String {idx} sent in the stream from first producer'
    data = data.encode('utf-8')
    attributes = {
        "string": string
    }
    print("The string published was", string)
    future = publisher.publish(topic_path, data, **attributes)
    print(f'published message to the topic ClassifyMe id {future.result()}')

    sleep(round(random.uniform(0.5, 2), 2))
    print('time taken', round(random.uniform(1, 4), 2))
    print('____________')
