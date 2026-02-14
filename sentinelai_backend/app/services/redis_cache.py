import os
import redis
import json

try:
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_password = os.getenv("REDIS_PASSWORD")
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_keepalive=True,
        health_check_interval=30
    )
    r.ping()  # Test connection
    print("[OK] Redis cache available")
except Exception as e:
    print(f"[WARN] Redis connection failed: {e}")
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
