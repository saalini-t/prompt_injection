import redis
import json

try:
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.ping()  # Test connection
except Exception as e:
    print(f"Redis connection failed: {e}")
    r = None

def get_cached_policy(text: str):
    if r is None:
        return None
    try:
        return r.get(text)
    except Exception as e:
        print(f"Redis GET error: {e}")
        return None

def set_cached_policy(text: str, result: dict):
    if r is None:
        return
    try:
        r.set(text, json.dumps(result), ex=60)  # 60 sec TTL
    except Exception as e:
        print(f"Redis SET error: {e}")
