from fastapi import APIRouter, WebSocket
from app.utils.logger import register_ws, unregister_ws
from app.utils.trace_bus import register_trace_ws, unregister_trace_ws

router = APIRouter()

@router.websocket("/attacks")
async def attack_feed(ws: WebSocket):
    await ws.accept()
    register_ws(ws)

    try:
        while True:
            await ws.receive_text()
    except:
        unregister_ws(ws)


@router.websocket("/trace")
async def trace_feed(ws: WebSocket):
    await ws.accept()
    register_trace_ws(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        unregister_trace_ws(ws)
