# simulator/main.py — จุดเริ่มต้นของ simulator
# รัน AGV agents, dispatcher, และ publisher พร้อมกัน

import asyncio
import httpx
import os
from dotenv import load_dotenv

# ลอง load .env หลายทางเผื่อ path ต่างกัน
load_dotenv("backend/.env")
load_dotenv("../backend/.env")

from simulator.agv_agent import AGVAgent
from simulator.dispatcher import Dispatcher
from simulator.publisher import PositionPublisher

API_URL   = os.getenv("API_URL",   "http://localhost:8000")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

print(f"API_URL: {API_URL}")
print(f"REDIS_URL: {REDIS_URL}")

async def load_agvs_from_db() -> list[AGVAgent]:
    """
    โหลดข้อมูล AGV จาก database ตอนเริ่มต้น
    เพื่อให้ simulator รู้ว่ามี AGV กี่ตัว อยู่ที่ไหน battery เท่าไหร่
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/api/v1/agvs", timeout=10.0, follow_redirects=True)
            print(f"Status: {response.status_code}")
            print(f"Body: {response.text[:200]}")  # แสดง 200 ตัวอักษรแรก

            if response.status_code != 200:
                raise Exception(f"API returned {response.status_code}: {response.text}")

            agvs_data = response.json()

        except httpx.ConnectError:
            raise Exception(f"Cannot connect to backend at {API_URL} — make sure uvicorn is running")

    agents = []
    for agv in agvs_data:
        agent = AGVAgent(
            agv_id  = agv["id"],
            name    = agv["name"],
            row     = agv["current_row"],
            col     = agv["current_col"],
            battery = agv["battery"],
            api_url = API_URL,
        )
        agents.append(agent)
    return agents

async def main():
    print("Starting AGV Simulator...")

    # โหลด AGV จาก database
    agents = await load_agvs_from_db()
    print(f"Loaded {len(agents)} AGVs: {[a.name for a in agents]}")

    # สร้าง dispatcher และ publisher
    dispatcher = Dispatcher(agents=agents, api_url=API_URL)
    publisher  = PositionPublisher(agents=agents, redis_url=REDIS_URL)

    # รันทุกอย่างพร้อมกัน
    await asyncio.gather(
        dispatcher.run(),   # poll tasks ทุก 2 วินาที
        publisher.run(),    # broadcast position ทุก 500ms
    )

if __name__ == "__main__":
    asyncio.run(main())