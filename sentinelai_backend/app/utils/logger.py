import time
import json
from app.db.mongo import attack_logs
from app.services.kafka_producer import publish_attack

_subscribers = []

def register_ws(ws):
    _subscribers.append(ws)

def unregister_ws(ws):
    if ws in _subscribers:
        _subscribers.remove(ws)

async def broadcast(event):
    for ws in _subscribers:
        try:
            await ws.send_text(json.dumps(event))
        except:
            pass

async def log_incident(event: dict):
    event["timestamp"] = int(time.time())

    result = attack_logs.insert_one(event)

    kafka_event = event.copy()
    kafka_event["_id"] = str(result.inserted_id)

    publish_attack(kafka_event)

    await broadcast(kafka_event)

