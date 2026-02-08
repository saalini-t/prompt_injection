import os, json, threading
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

producer = None
_init_lock = threading.Lock()
_init_failed = False

def _get_producer():
    global producer, _init_failed
    
    if _init_failed:
        return None
    
    if producer is not None:
        return producer
    
    with _init_lock:
        if producer is not None:
            return producer
        
        try:
            conf = {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP", ""),
                "security.protocol": "SASL_SSL",
                "sasl.mechanisms": "PLAIN",
                "sasl.username": os.getenv("KAFKA_API_KEY", ""),
                "sasl.password": os.getenv("KAFKA_API_SECRET", ""),
                "client.id": "sentinelai-producer",
                "socket.timeout.ms": 5000,
                "debug": "broker,security"
            }
            
            # Skip Kafka if no credentials
            if not conf["bootstrap.servers"] or not conf["sasl.username"]:
                print("⚠️  Kafka not configured, skipping")
                _init_failed = True
                return None
            
            producer = Producer(conf)
            print("✅ Kafka producer initialized")
            return producer
        except Exception as e:
            print(f"⚠️  Kafka initialization failed (non-blocking): {e}")
            _init_failed = True
            return None

def delivery_report(err, msg):
    if err:
        print("❌ Kafka delivery failed:", err)
    else:
        print("✅ Kafka delivered:", msg.topic(), msg.offset())

def publish_attack(event: dict):
    try:
        producer_instance = _get_producer()
        if producer_instance is None:
            print("⚠️  Kafka unavailable, skipping publish")
            return
        
        print("📤 Sending to Kafka:", event)
        producer_instance.produce(
            topic="sentinel.attacks",
            value=json.dumps(event),
            callback=delivery_report
        )
        producer_instance.flush(5)
    except Exception as e:
        print(f"⚠️  Publish error: {e}")

