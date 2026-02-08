import sys
sys.path.insert(0, r"c:\Saalu_Data\prompt_injection\sentinelai_backend")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.detector import hybrid_detect
from app.core.prompt_sanitizer import sanitize_prompt
from app.api.v1 import routes_simulator, routes_ws
from app.utils.trace_bus import emit_trace
from app.utils.logger import broadcast
import redis
import json
import time

app = FastAPI(title="SentinelAI Test Server - 3 Brain System")

# Test Redis
try:
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.ping()
    redis_available = True
    print("✅ Redis cache available")
except:
    redis_available = False
    r = None
    print("⚠️  Redis cache unavailable")

def get_cached_policy(text):
    if not redis_available:
        return None
    try:
        return r.get(text)
    except:
        return None

def set_cached_policy(text, result):
    if not redis_available:
        return
    try:
        r.set(text, json.dumps(result), ex=60)
    except:
        pass

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include simulator routes and websockets
app.include_router(routes_simulator.router, prefix="/api/v1/simulator", tags=["Simulator"])
app.include_router(routes_ws.router)

@app.post("/api/v1/detect/scan")
async def scan_prompt(payload: dict):
    """3-brain hybrid detection endpoint"""
    text = payload.get("text", "")
    
    if not text:
        return {"error": "No text provided"}
    
    # Emit trace: Request received
    await emit_trace("Request received", {"text": text[:100] + "..." if len(text) > 100 else text})
    
    # Check cache
    if redis_available:
        cached = get_cached_policy(text)
        if cached:
            print(f"✅ Cache HIT for: {text[:50]}...")
            await emit_trace("Cache HIT", {"cached": True})
            return {"cached": True, "result": json.loads(cached)}
        else:
            print(f"❌ Cache MISS for: {text[:50]}...")
            await emit_trace("Cache MISS", {"cached": False})
    
    # Emit trace: Starting detection
    await emit_trace("Starting 3-brain detection", {
        "brains": ["Injection", "Ethics", "Narrative"]
    })
    
    # Run 3-brain hybrid detection
    hybrid_result = hybrid_detect(text)
    
    # Emit trace: Detection complete
    await emit_trace("Detection complete", {
        "injection_score": hybrid_result.get("injection", {}).get("ml_score", 0),
        "ethics_confidence": hybrid_result.get("ethics", {}).get("confidence", 0),
        "narrative_confidence": hybrid_result.get("narrative", {}).get("confidence", 0),
        "final_risk": hybrid_result.get("risk", 0),
        "decision": hybrid_result.get("decision", "unknown")
    })
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_numpy_types(obj):
        """Recursively convert numpy types to native Python types"""
        if isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        elif hasattr(obj, 'item'):  # numpy scalar
            return obj.item()
        elif isinstance(obj, (bool, int, float, str)) or obj is None:
            return obj
        else:
            return str(obj)
    
    hybrid_result = convert_numpy_types(hybrid_result)
    
    sanitized = None
    if hybrid_result["decision"] == "sanitize":
        await emit_trace("Sanitizing prompt", {"reason": "Medium risk detected"})
        sanitized = sanitize_prompt(text)
        await emit_trace("Sanitization complete", {"sanitized": sanitized[:100] + "..." if sanitized and len(sanitized) > 100 else sanitized})
    
    result = {
        "hybrid_analysis": hybrid_result,
        "sanitized": sanitized
    }
    
    # Broadcast attack event to WebSocket clients
    decision = hybrid_result.get("decision", "unknown")
    if decision in ["block", "sanitize"]:
        attack_event = {
            "timestamp": int(time.time()),
            "text": text,
            "decision": decision,
            "risk": hybrid_result.get("risk", 0),
            "triggered_by": hybrid_result.get("triggered_by", []),
            "injection": hybrid_result.get("injection", {}),
            "ethics": hybrid_result.get("ethics", {}),
            "narrative": hybrid_result.get("narrative", {})
        }
        await broadcast(attack_event)
        await emit_trace("Attack logged and broadcast", {"decision": decision, "risk": hybrid_result.get("risk", 0)})
    else:
        await emit_trace("Request allowed", {"decision": "allow"})
    
    # Cache result
    if redis_available:
        set_cached_policy(text, result)
        await emit_trace("Result cached", {"ttl": 60})
    
    return {"cached": False, "result": result}

if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("🚀 Starting SentinelAI 3-Brain Detection Server")
    print("=" * 80)
    print("✅ Hybrid detection ready (Injection + Ethics + Narrative)")
    print("🌐 Server: http://127.0.0.1:8002")
    print("=" * 80)
    uvicorn.run(app, host="127.0.0.1", port=8002)
