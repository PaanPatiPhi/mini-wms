# agv_agent.py — จำลองการทำงานของ AGV 1 ตัว
# ใช้ asyncio ทำให้ AGV หลายตัวทำงานพร้อมกันได้

import asyncio
import httpx # ใช้เรียก FASTAPI API
from simulator.pathfinder import bfs

# States ทั้งหมดของ AGV
IDLE        = "idle"
MOVING      = "moving"
PICKING     = "picking"
DELIVERING  = "delivering"
CHARGING    = "charging"

# ค่า config
STEP_DELAY      = 0.5   # วินาที ต่อ 1 cell ที่เดิน
PICK_DELAY      = 2.0   # วินาที ใช้เวลา pick ของ
DELIVER_DELAY   = 1.5   # วินาที ใช้เวลา deliver ของ
LOW_BATTERY     = 15.0  # % ที่ต้องกลับไปชาร์จ
BATTERY_DRAIN   = 0.5   # % ต่อการเดิน 1 cell
BATTERY_CHARGE  = 1.0   # % ต่อวินาทีที่ชาร์จ

# Charging stations ในระบบ
CHARGE_STATIONS = [(11, 0), (11, 1), (11, 2)]

class AGVAgent:
    def __init__(self, agv_id:int, name: str, row:int, col:int, battery:float, api_url:str):
        self.agv_id = agv_id
        self.name = name
        self.row = row
        self.col = col
        self.battery = battery
        self.state = IDLE
        self.task = None # task ที่ทำอยู่
        self.cargo = None # cargo ที่ถืออยู่
        self.api_url = api_url # URL ของ FastAPI

    async def update_state_in_db(self, state:str = None):
        """
        อัปเดต state, position, battery ลง database ผ่าน API
        simulator คุยกับ backend ผ่าน HTTP 
        """
        async with httpx.AsyncClient() as client:
            await client.patch(
                f"{self.api_url}/api/v1/agvs/{self.agv_id}/state",
                json={
                    "state": state or self.state,
                    "battery": round(self.battery, 1),
                    "current_row": self.row,
                    "current_col": self.col,
                }
            )

    async def move_to(self, goal_row: int, goal_col:int, other_positions:list):
        """
        เดินไปยัง goal ทีละ cell
        other_positions คือตำแหน่ง AGV ตัวอื่น ใช้หลีกเลี่ยง collision
        """
        path = bfs(
            start =(self.row, self.col),
            goal = (goal_row, goal_col),
            obstacles=other_positions
        )

        # เดินทีละ cell ตาม path
        for step_row, step_col in path[1:]: #skip จุดเริ่มต้น
            self.row = step_row
            self.col = step_col
            self.battery = max(0, self.battery - BATTERY_DRAIN)
            await self.update_state_in_db(MOVING)
            await asyncio.sleep(STEP_DELAY)

    async def execute_task(self, task: dict, other_positions: list):
        """
        ทำ task ตาม phase:
        1. เดินไปรับของที่ from_location
        2. หยุด pick ของ
        3. เดินไปส่งที่ to_location
        4. หยุด deliver ของ
        5. กลับ idle
        """
        self.task = task
        from_row = task["from_row"]
        from_col = task["from_col"]
        to_row = task["to_row"]
        to_col = task["to_col"]

        # Phase 1: เดินไปรับของ
        self.state = MOVING
        await self.move_to(from_row, from_col, other_positions)

        # Phase 2: หยุด pick ของ
        self.state = PICKING
        self.cargo = task["task_id"]
        await self.update_state_in_db(PICKING)
        await asyncio.sleep(PICK_DELAY)

        # Phase 3: เดินไปส่งของ
        self.state = DELIVERING
        await self.move_to(to_row, to_col, other_positions)

        # Phase 4: หยุด deliver ของ
        self.state = DELIVERING
        await self.update_state_in_db(DELIVERING)
        await asyncio.sleep(DELIVER_DELAY)

        # Phase 5: task เสร็จ
        self.cargo = None
        self.task  = None
        self.state = IDLE
        await self.update_state_in_db(IDLE)  # ✅ แก้จาก DELIVER_DELAY เป็น IDLE

        # อัปเดต task status ใน database
        async with httpx.AsyncClient() as client:
            await client.patch(
                f"{self.api_url}/api/v1/tasks/{task['task_id']}/status?status=done",
                follow_redirects=True  # เพิ่มด้วยเผื่อ 307
            )

    async def go_charge(self, other_positions: list):
        """กลับไปชาร์จที่ charging station"""
        # หา charging station ที่ว่าง
        charge_pos = CHARGE_STATIONS[self.agv_id % len(CHARGE_STATIONS)]
        self.state = MOVING
        await self.move_to(charge_pos[0], charge_pos[1], other_positions)

        # ชาร์จจนเต็ม
        self.state = CHARGING
        while self.battery < 100.0:
            self.battery = min(100.0, self.battery + BATTERY_CHARGE)
            await self.update_state_in_db(CHARGING)
            await asyncio.sleep(1.0)

        self.state = IDLE
        await self.update_state_in_db(IDLE)

    def get_position(self) -> dict:
        """คืน position ปัจจุบัน สำหรับ broadcast ผ่าน Redis"""
        return {
            "agv_id": self.agv_id,
            "name": self.name,
            "row": self.row,
            "col": self.col,
            "state": self.state,
            "battery": round(self.battery, 1),
            "cargo": self.cargo,
        }