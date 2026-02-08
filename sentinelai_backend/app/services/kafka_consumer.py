import os, json
from confluent_kafka import Consumer
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

conf = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP"),
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.getenv("KAFKA_API_KEY"),
    "sasl.password": os.getenv("KAFKA_API_SECRET"),
    "group.id": "sentinelai-analytics",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(conf)
consumer.subscribe(["sentinel.attacks"])

attack_counts = defaultdict(int)

print("📡 Kafka Analytics Consumer started...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("❌ Kafka error:", msg.error())
        continue

    event = json.loads(msg.value().decode("utf-8"))

    attack_counts[event["decision"]] += 1

    print("📊 LIVE METRICS:", dict(attack_counts))
