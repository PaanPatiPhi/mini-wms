# publisher.py — broadcast ตำแหน่ง AGV ทุก 500ms ผ่าน Redis Pub/Sub
# frontend จะรับข้อมูลนี้ผ่าน WebSocket

import asyncio
import json
import redis.asyncio as aioredis

class PositionPublisher:
    def __init__(self, agents: list, redis_url: str):
        self.agents    = agents
        self.redis_url = redis_url
        self.redis     = None

    async def connect(self):
        """เชื่อมต่อ Redis"""
        self.redis = await aioredis.from_url(self.redis_url)
        print("Publisher connected to Redis")

    async def run(self):
        """
        loop broadcast ตำแหน่ง AGV ทุก 500ms
        ส่งไปที่ Redis channel ชื่อ 'agv:positions'
        FastAPI WebSocket จะ subscribe channel นี้แล้ว forward ไปหา frontend
        """
        await self.connect()
        while True:
            # รวบรวมตำแหน่งทุก AGV
            positions = [agent.get_position() for agent in self.agents]
            # ส่งเป็น JSON ไปที่ Redis channel
            await self.redis.publish(
                "agv:positions",
                json.dumps(positions)
            )
            await asyncio.sleep(0.5)