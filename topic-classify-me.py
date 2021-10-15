from src.classifier import ClassfiyStrings
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

private_key_path = 'PATH_TO_YOUR_PRIVATE_KEY'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key_path

# first lets subscribe to the producers

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'YOUR_SUBSCRIPTION_PATH_FOR_CLASSIFYME_TOPIC'


def callback(message):
    print(f'Received message: {message.data}')
    if message.attributes:
        print("Attributes:")
        string_received = ''
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")
            string_received = value
        print("Classifying the string received")
        classification_of_string = ClassfiyStrings(string_received).run()

        # publish this to the topic FindDuplicate

        publisher_for_find_duplicate = pubsub_v1.PublisherClient()
        topic_path = 'YOUR_PUBLICATION_PATH_FOR_FINDDUPLICATE_TOPIC'

        data = "String and the classification of it was sent to FindDuplicate topic"
        data = data.encode('utf-8')
        attributes = {
            "string": string_received,
            "category": classification_of_string
        }
        # print(classification_of_string)
        future = publisher_for_find_duplicate.publish(topic_path, data, **attributes)
        print(f'published message to the topic ClassifyMe id {future.result()}')
        print('______________________________________________________________')
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')

with subscriber:
    try:
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()  # going without a timeout will wait & block indefinitely
        # streaming_pull_future.
    except TimeoutError:
        streaming_pull_future.cancel()  # trigger the shutdown
        streaming_pull_future.result()  # block until the shutdown is complete
