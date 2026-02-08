import json
import time
from typing import Dict, Any

# Trace subscribers for live execution trace websocket
_trace_subscribers = []


def register_trace_ws(ws):
    _trace_subscribers.append(ws)


def unregister_trace_ws(ws):
    if ws in _trace_subscribers:
        _trace_subscribers.remove(ws)


async def emit_trace(step: str, meta: Dict[str, Any] | None = None):
    """
    Broadcast a single trace step to all connected WebSocket clients.
    Each event includes a timestamp, step label, and optional metadata.
    """
    event = {
        "step": step,
        "meta": meta or {},
        "ts": int(time.time()),
    }

    # Broadcast to all subscribers; ignore broken connections
    for ws in list(_trace_subscribers):
        try:
            await ws.send_text(json.dumps(event))
        except Exception:
            try:
                _trace_subscribers.remove(ws)
            except ValueError:
                pass
