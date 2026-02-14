import json
from fastapi import APIRouter
from app.core.detector import hybrid_detect
from app.core.policy_engine import evaluate_policy
from app.core.prompt_sanitizer import sanitize_prompt
from app.core.ethics_guardian import ethics_check

# Optionally import logger - gracefully degrade if dependencies unavailable
try:
    from app.utils.logger import log_incident
    logger_available = True
except:
    logger_available = False
    async def log_incident(data): pass

# Optional Redis cache - gracefully degrade if not available
try:
    from app.services.redis_cache import get_cached_policy, set_cached_policy
    # Test Redis connection
    import redis
    _redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    _redis_client.ping()
    redis_available = True
    print("[OK] Redis cache available")
except Exception as e:
    print(f"[WARN] Redis cache unavailable: {e}")
    redis_available = False
    def get_cached_policy(text): return None
    def set_cached_policy(text, result): pass

router = APIRouter()


def _convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {k: _convert_numpy_types(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_numpy_types(item) for item in obj]
    if hasattr(obj, "item"):
        try:
            return obj.item()
        except Exception:
            return str(obj)
    if isinstance(obj, (bool, int, float, str)) or obj is None:
        return obj
    return str(obj)

@router.post("/scan")
async def scan_prompt(payload: dict):
    try:
        text = payload.get("text", "")
        
        if not text:
            return {"error": "No text provided", "status": "failed"}

        if redis_available:
            cached = get_cached_policy(text)
            if cached:
                print(f"[OK] Cache HIT for: {text[:50]}...")
                return {"cached": True, "result": json.loads(cached)}
            else:
                print(f"[MISS] Cache MISS for: {text[:50]}...")

        # Run 3-brain hybrid detection
        hybrid_result = _convert_numpy_types(hybrid_detect(text))
        ethics_result = ethics_check(text)

        if ethics_result.get("ethical_risk"):
            hybrid_result["decision"] = "block"
            hybrid_result["risk"] = max(hybrid_result.get("risk", 0), ethics_result.get("score", 0.9))
        
        sanitized = None
        if hybrid_result["decision"] == "sanitize":
            sanitized = sanitize_prompt(text)

        # Log all prompts (audit trail)
        if logger_available:
            try:
                await log_incident({
                    "text": text,
                    "decision": hybrid_result["decision"],
                    "risk": hybrid_result["risk"],
                    "triggered_by": hybrid_result["triggered_by"],
                    "injection_confidence": hybrid_result["injection"]["confidence"],
                    "ethics_confidence": hybrid_result["ethics"]["confidence"],
                    "narrative_confidence": hybrid_result["narrative"]["confidence"],
                    "original": text
                })
            except Exception as log_err:
                print(f"Logging error (non-blocking): {log_err}")

        result = {
            "hybrid_analysis": hybrid_result,
            "ethics_analysis": ethics_result,
            "sanitized": sanitized,
            "timestamp": None  # Add timestamp if needed
        }

        result = _convert_numpy_types(result)

        if redis_available:
            try:
                set_cached_policy(text, result)
            except Exception as cache_err:
                print(f"Cache set error: {cache_err}")

        return {"cached": False, "result": result}
    
    except Exception as e:
        print(f"Scan error: {e}")
        return {"error": str(e), "status": "failed"}

