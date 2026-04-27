# ws.py — WebSocket endpoint สำหรับ frontend เชื่อมต่อรับ AGV position real-time

import asyncio
import json
import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import os

router = APIRouter(tags=["WebSocket"])

class ConnectionManager:
    """จัดการ WebSocket clients ที่ connect อยู่ทั้งหมด"""
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """ส่งข้อมูลไปทุก client ที่ connect อยู่"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass  # ถ้า client disconnect แล้วก็ข้ามไป

manager = ConnectionManager()

@router.websocket("/ws/agv")
async def agv_websocket(websocket: WebSocket):
    """
    Frontend connect มาที่ ws://localhost:8000/ws/agv
    แล้วจะได้รับ AGV positions ทุก 500ms
    """
    await manager.connect(websocket)
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

    try:
        # Subscribe Redis channel
        redis = await aioredis.from_url(redis_url)
        pubsub = redis.pubsub()
        await pubsub.subscribe("agv:positions")

        # รับข้อมูลจาก Redis แล้ว forward ไปหา frontend
        async for message in pubsub.listen():
            if message["type"] == "message":
                await manager.broadcast(message["data"].decode())

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)