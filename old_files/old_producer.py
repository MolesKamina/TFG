from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('sensor_input', b'Hello, Kafka!')
producer.flush()
