import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

private_key_path = 'PATH_TO_YOUR_PRIVATE_KEY'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key_path

# first lets subscribe to the producers

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'YOUR_SUBSCRIPTION_PATH_FOR_ClusteringOfStrings_TOPIC'


def callback(message):
    print(f'Received message: {message.data}')

    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")
            print('______________________________________________________________')

    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')

with subscriber:
    try:
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()  # going without a timeout will wait & block indefinitely
    except TimeoutError:
        streaming_pull_future.cancel()  # trigger the shutdown
        streaming_pull_future.result()  # block until the shutdown is complete
