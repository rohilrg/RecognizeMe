import json

from src.duplicate_finder import FindDuplicate
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

private_key_path = 'PATH_TO_YOUR_PRIVATE_KEY'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key_path

# first lets subscribe to the producers

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'YOUR_SUBSCRIPTION_PATH_FOR_FINDDUPLICATE_TOPIC'

duplicate_finder = FindDuplicate()


def callback(message):
    print(f'Received message: {message.data}')
    if message.attributes:
        print("Attributes:")
        dict_for_finding_duplicate_for_new_string = message.attributes

        print("find duplicate in the dict")
        updated_dict = duplicate_finder.run_checker(dict_for_finding_duplicate_for_new_string)

        # publish this to the topic Clusteringofstrings

        publisher_for_clustering_of_strings = pubsub_v1.PublisherClient()
        topic_path = 'YOUR_PUBLICATION_PATH_FOR_ClusteringOfStrings_TOPIC'

        data = "Updated version of string in proper clustering"
        data = data.encode('utf-8')
        attributes = {"cluster_of_strings": json.dumps(updated_dict)}
        # print(classification_of_string)
        future = publisher_for_clustering_of_strings.publish(topic_path, data, **attributes)
        print(f'published message to the topic FindDuplicate id {future.result()}')
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
