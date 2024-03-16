from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
import sys

admin_client = KafkaAdminClient(bootstrap_servers=['192.168.10.181:9092'])

def create_topics(topic_names):
    existing_topic_list = consumer.topics()
    print(list(consumer.topics()))
    topic_list = []
    for topic in topic_names:
        if topic not in existing_topic_list:
            print('Topic : {} added '.format(topic))
            topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
        else:
            print('Topic : '+ topic +' already exist ')
    try:
        if topic_list:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print("Topic Created Successfully")
        else:
            print("Topic Exist")
    #except TopicAlreadyExistsError as e:
    #    print("Topic Already Exist")
    except  Exception as e:
        print(e)

def delete_topics(topic_names):
    try:
        admin_client.delete_topics(topics=topic_names)
        print("Topic Deleted Successfully")
    #except UnknownTopicOrPartitionError as e:
    #    print("Topic Doesn't Exist")
    except  Exception as e:
        print(e)


consumer = KafkaConsumer(
    bootstrap_servers = "192.168.10.181:9092",
    )

print("Basic topic administrator")

action = int(sys.argv[1])
path = str(sys.argv[2])

topics = []
with open(path) as list_topics:
    for a in list_topics:
        topics.append(a.strip())
if action == 1:
    delete_topics(topics)
else:
    create_topics(topics)

print("All actions done")