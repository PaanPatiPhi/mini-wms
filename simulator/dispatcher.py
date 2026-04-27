# dispatcher.py — ดึง task จาก database แล้ว assign ให้ AGV
# รันเป็น background loop ทุก 2 วินาที

import asyncio
import httpx
from simulator.agv_agent import AGVAgent, LOW_BATTERY

class Dispatcher:
    def __init__(self, agents: list[AGVAgent], api_url: str):
        self.agents  = agents
        self.api_url = api_url

    def get_other_positions(self, exclude_id: int) -> list:
        """คืน list ตำแหน่งของ AGV ตัวอื่น ใช้สำหรับหลีกเลี่ยง collision"""
        return [
            (a.row, a.col)
            for a in self.agents
            if a.agv_id != exclude_id
        ]

    async def fetch_queued_tasks(self) -> list:
        """ดึง tasks ที่ status=queued จาก API"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/api/v1/tasks/",
                params={"status": "queued"},
                follow_redirects=True  # ป้องกัน 307 redirect
            )
            if response.status_code == 200:
                return response.json()
            print(f"[Dispatcher] fetch_queued_tasks failed: {response.status_code}")
            return []

    async def fetch_task_locations(self, task: dict) -> dict | None:
        async with httpx.AsyncClient() as client:
            from_res = await client.get(
                f"{self.api_url}/api/v1/locations/{task['from_location_id']}",
                follow_redirects=True
            )
            to_res = await client.get(
                f"{self.api_url}/api/v1/locations/{task['to_location_id']}",
                follow_redirects=True
            )

            print(f"[Dispatcher] from_res: {from_res.status_code} | to_res: {to_res.status_code}")

            if from_res.status_code == 200 and to_res.status_code == 200:
                from_loc = from_res.json()
                to_loc   = to_res.json()
                return {
                    "task_id":  task["id"],
                    "from_row": from_loc["row"],
                    "from_col": from_loc["col"],
                    "to_row":   to_loc["row"],
                    "to_col":   to_loc["col"],
                }
            else:
                print(f"[Dispatcher] from body: {from_res.text[:100]}")
                print(f"[Dispatcher] to body: {to_res.text[:100]}")
        return None

    async def run(self):
        """
        Main loop ของ dispatcher
        ทุก 2 วินาที ดึง tasks ใหม่แล้ว assign ให้ AGV ที่ว่าง
        """
        while True:
            tasks = await self.fetch_queued_tasks()
            print(f"[Dispatcher] queued tasks: {len(tasks)}")

            # เรียง priority: high → mid → low
            priority_order = {"high": 0, "mid": 1, "low": 2}
            tasks.sort(key=lambda t: priority_order.get(t.get("priority", "mid"), 1))

            for task in tasks:
                # หา AGV ที่ idle และ battery พอ
                idle_agent = next(
                    (a for a in self.agents
                     if a.state == "idle" and a.battery > LOW_BATTERY),
                    None
                )
                print(f"[Dispatcher] task #{task['id']} → idle_agent: {idle_agent.name if idle_agent else None}")

                if not idle_agent:
                    break

                task_data = await self.fetch_task_locations(task)
                print(f"[Dispatcher] task_data: {task_data}")

                if not task_data:
                    continue

                # อัปเดต task status เป็น running
                async with httpx.AsyncClient() as client:
                    res = await client.patch(
                        f"{self.api_url}/api/v1/tasks/{task['id']}/status",
                        params={"status": "running"},
                        follow_redirects=True
                    )
                    print(f"[Dispatcher] patch task status: {res.status_code}")

                # สั่งให้ AGV ทำ task (รัน background ไม่รอเสร็จ)
                other_pos = self.get_other_positions(idle_agent.agv_id)
                asyncio.create_task(idle_agent.execute_task(task_data, other_pos))

            # เช็ค AGV ที่ battery ต่ำ
            for agent in self.agents:
                if agent.state == "idle" and agent.battery < LOW_BATTERY:
                    other_pos = self.get_other_positions(agent.agv_id)
                    asyncio.create_task(agent.go_charge(other_pos))

            await asyncio.sleep(2.0)