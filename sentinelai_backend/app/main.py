from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes_detect, routes_tools, routes_ws, routes_llm, routes_policy, routes_metrics, routes_simulator, routes_security

# Try to import vision router (optional)
try:
    from app.vision.vision_router import router as vision_router
    vision_available = True
except Exception as e:
    print(f"[WARN] Vision router unavailable: {e}")
    vision_available = False
    vision_router = None

from app.api.v1 import routes_security

app = FastAPI(title="SentinelAI Firewall")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_detect.router, prefix="/api/v1/detect")
app.include_router(routes_tools.router, prefix="/api/v1/tools")
app.include_router(routes_ws.router)   # ← THIS LINE WAS MISSING
app.include_router(routes_llm.router, prefix="/api/v1/llm")
app.include_router(routes_policy.router, prefix="/api/v1/policy")
app.include_router(routes_metrics.router, prefix="/api/v1/metrics")
app.include_router(routes_simulator.router, prefix="/api/v1/simulator")
app.include_router(routes_security.router, prefix="/api/v1/security")
if vision_available and vision_router:
    app.include_router(vision_router, prefix="/api/v1/vision") 