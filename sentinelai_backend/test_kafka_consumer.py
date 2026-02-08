import os, sys
sys.path.insert(0, r"c:\Saalu_Data\prompt_injection\sentinelai_backend")

import json
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
    "group.id": "sentinelai-analytics-test",
    "auto.offset.reset": "earliest"
}

print("Connecting to Kafka...")
consumer = Consumer(conf)
consumer.subscribe(["sentinel.attacks"])

attack_counts = defaultdict(int)

print("[OK] Kafka Analytics Consumer started - listening for messages...")
print("Press CTRL+C to stop\n")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            print(".", end="", flush=True)
            continue
        if msg.error():
            print(f"\n[ERROR] Kafka error: {msg.error()}")
            continue

        event = json.loads(msg.value().decode("utf-8"))
        attack_counts[event["decision"]] += 1

        print(f"\n[RECEIVED] Attack event: {event}")
        print(f"[METRICS] {dict(attack_counts)}")
except KeyboardInterrupt:
    print("\n\n[STOP] Consumer stopped by user")
finally:
    consumer.close()
    print("[CLOSED] Kafka consumer closed")
