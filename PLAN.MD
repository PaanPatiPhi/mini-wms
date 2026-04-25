# Mini WMS — Project Plan

> ระบบจำลอง Warehouse Management System พร้อม Mock AGV สำหรับ Portfolio

**Stack:** FastAPI · PostgreSQL · Redis · React · TypeScript · Docker  
**Deploy:** Railway (backend) · Vercel (frontend)  
**ระยะเวลารวม:** ~10–14 สัปดาห์

---

## สถานะปัจจุบัน

- [x] ติดตั้ง Python, Docker Desktop
- [x] สร้าง project structure
- [x] FastAPI skeleton รันได้ (`/` และ `/health`)
- [x] `.env`, `.gitignore`, `requirements.txt` ครบ
- [x] Push ขึ้น GitHub แล้ว

---

## Phase 1 — Foundation & Data Model
> สัปดาห์ 1–2 | สถานะ: 🟡 กำลังทำ

### 1.1 Docker Compose
- [ ] สร้างไฟล์ `docker-compose.yml` ที่ root
- [ ] Define service `postgres` (image: postgres:15, env: DB name/user/pass, volume)
- [ ] Define service `redis` (image: redis:7)
- [ ] Define service `backend` (build: ./backend, port 8000, depends_on postgres+redis)
- [ ] เพิ่ม healthcheck ให้ postgres
- [ ] รัน `docker compose up` แล้วทดสอบว่า backend ต่อ postgres ได้

### 1.2 Dockerfile สำหรับ Backend
- [ ] สร้าง `backend/Dockerfile`
- [ ] ใช้ `python:3.12-slim` เป็น base image
- [ ] COPY requirements.txt แล้ว `pip install`
- [ ] COPY app/ และ set CMD เป็น uvicorn

### 1.3 Database Schema (SQLAlchemy Models)
- [ ] สร้างไฟล์ `app/models/__init__.py`
- [ ] สร้าง `app/models/product.py` — ตาราง products (id, sku, name, description, weight, created_at)
- [ ] สร้าง `app/models/location.py` — ตาราง locations (id, code, zone, row, col, type: shelf/inbound/outbound/charge)
- [ ] สร้าง `app/models/inventory.py` — ตาราง inventory (id, product_id, location_id, quantity, updated_at)
- [ ] สร้าง `app/models/agv.py` — ตาราง agvs (id, name, state, battery, current_row, current_col, created_at)
- [ ] สร้าง `app/models/order.py` — ตาราง orders (id, status, created_at, completed_at)
- [ ] สร้าง `app/models/order_item.py` — ตาราง order_items (id, order_id, product_id, quantity, picked)
- [ ] สร้าง `app/models/task.py` — ตาราง tasks (id, agv_id, order_id, from_location_id, to_location_id, status, priority, created_at, completed_at)
- [ ] สร้าง `app/models/agv_log.py` — ตาราง agv_logs (id, agv_id, task_id, from_row, from_col, to_row, to_col, timestamp)

### 1.4 Alembic Migration
- [ ] รัน `alembic init alembic` ใน backend/
- [ ] แก้ `alembic/env.py` ให้ import Base จาก models
- [ ] รัน `alembic revision --autogenerate -m "initial tables"`
- [ ] รัน `alembic upgrade head` เพื่อสร้าง table จริงใน postgres

### 1.5 Seed Data
- [ ] สร้าง `app/seed.py`
- [ ] Seed products 10 รายการ (ชื่อ, SKU, น้ำหนัก)
- [ ] Seed locations ตาม warehouse grid (shelves A1–I8, inbound, outbound, charging)
- [ ] Seed inventory (กระจายสินค้าไปตาม shelf ต่าง ๆ)
- [ ] Seed AGV 3 ตัว (AGV-01, AGV-02, AGV-03) state=idle, battery=100

### 1.6 README เบื้องต้น
- [ ] สร้าง `README.md` ที่ root
- [ ] เขียน: Project overview, Tech stack, Local setup guide (`docker compose up`)
- [ ] เพิ่ม architecture diagram (ทำทีหลังได้)

**Deliverable:** `docker compose up` แล้วระบบทั้งหมดขึ้น, table ครบใน postgres, seed data พร้อม

---

## Phase 2 — Core WMS API
> สัปดาห์ 3–5 | สถานะ: ⬜ ยังไม่เริ่ม

### 2.1 Schemas (Pydantic)
- [ ] สร้าง `app/schemas/product.py` — ProductCreate, ProductRead
- [ ] สร้าง `app/schemas/location.py` — LocationRead
- [ ] สร้าง `app/schemas/inventory.py` — InventoryRead, InventoryUpdate
- [ ] สร้าง `app/schemas/order.py` — OrderCreate, OrderRead, OrderStatus
- [ ] สร้าง `app/schemas/task.py` — TaskCreate, TaskRead, TaskStatus
- [ ] สร้าง `app/schemas/agv.py` — AGVRead, AGVStatus

### 2.2 Inventory API
- [ ] สร้าง `app/routers/inventory.py`
- [ ] `GET /inventory` — ดูสินค้าทั้งหมดพร้อม location
- [ ] `GET /inventory/{product_id}` — ดูสินค้าชิ้นนั้น
- [ ] `PUT /inventory/{id}` — อัปเดต quantity
- [ ] `GET /inventory/low-stock` — สินค้าที่ quantity < threshold

### 2.3 Order API
- [ ] สร้าง `app/routers/orders.py`
- [ ] `POST /orders` — สร้าง order พร้อม items
- [ ] `GET /orders` — ดู order ทั้งหมด (filter by status)
- [ ] `GET /orders/{id}` — ดู order detail พร้อม items
- [ ] `PATCH /orders/{id}/status` — อัปเดต status (pending → picking → packed → dispatched)
- [ ] Auto-generate pick list เมื่อสร้าง order (หา location ของแต่ละ product อัตโนมัติ)

### 2.4 AGV API
- [ ] สร้าง `app/routers/agvs.py`
- [ ] `GET /agvs` — ดู AGV ทั้งหมดพร้อม state
- [ ] `GET /agvs/{id}` — ดู AGV ชิ้นนั้น
- [ ] `PATCH /agvs/{id}/state` — อัปเดต state (สำหรับ simulator ใช้)

### 2.5 Task API
- [ ] สร้าง `app/routers/tasks.py`
- [ ] `POST /tasks` — สร้าง task (from, to, priority, agv_id)
- [ ] `GET /tasks` — ดู task ทั้งหมด (filter by status/agv)
- [ ] `GET /tasks/{id}` — ดู task detail
- [ ] `PATCH /tasks/{id}/status` — อัปเดต status
- [ ] Auto-assign: หา AGV ที่ idle แล้ว assign ให้อัตโนมัติ

### 2.6 Register Routers ใน main.py
- [ ] `include_router` ทุก router ใน `main.py`
- [ ] เพิ่ม prefix เช่น `/api/v1/orders`

### 2.7 Authentication (JWT)
- [ ] ลง `pip install python-jose[cryptography] passlib[bcrypt]`
- [ ] สร้าง `app/models/user.py` — ตาราง users (id, email, hashed_password, role)
- [ ] สร้าง `app/routers/auth.py`
- [ ] `POST /auth/register` — สมัครสมาชิก
- [ ] `POST /auth/login` — login รับ JWT token กลับมา
- [ ] สร้าง dependency `get_current_user` สำหรับ protect routes

### 2.8 Testing
- [ ] ลง `pip install pytest httpx`
- [ ] สร้าง `tests/test_orders.py` — ทดสอบ create order, get order
- [ ] สร้าง `tests/test_inventory.py` — ทดสอบ get inventory
- [ ] รัน `pytest` ให้ผ่านทุก test

**Deliverable:** Swagger UI ครบทุก endpoint, ทดสอบผ่าน Swagger ได้, pytest ผ่าน

---

## Phase 3 — AGV Simulator + Real-time
> สัปดาห์ 6–8 | สถานะ: ⬜ ยังไม่เริ่ม

### 3.1 Warehouse Grid
- [ ] สร้าง `simulator/grid.py`
- [ ] Define ROWS=12, COLS=16
- [ ] Map cell types: 0=aisle, 1=shelf, 2=inbound, 3=outbound, 4=charge
- [ ] ตรงกับ location table ใน database

### 3.2 BFS Pathfinding
- [ ] สร้าง `simulator/pathfinder.py`
- [ ] เขียน function `bfs(start, goal, obstacles)` คืน list of (row, col)
- [ ] รองรับ obstacle = ตำแหน่ง AGV ตัวอื่น
- [ ] เขียน unit test สำหรับ pathfinder

### 3.3 AGV State Machine
- [ ] สร้าง `simulator/agv_agent.py`
- [ ] States: `idle → moving → picking → delivering → returning → charging`
- [ ] ใช้ `asyncio` loop เดิน AGV ทีละ cell ทุก 500ms
- [ ] Battery drain ระหว่างเคลื่อนที่ (ลดครั้งละ 0.5%)
- [ ] Auto-dock เมื่อ battery < 15% และ idle

### 3.4 Task Dispatcher
- [ ] สร้าง `simulator/dispatcher.py`
- [ ] Poll tasks จาก database ที่ status=queued ทุก 2 วินาที
- [ ] หา AGV ที่ idle และ battery > 20%
- [ ] Assign task → อัปเดต task.status=running, agv.state=moving
- [ ] Priority: high → mid → low

### 3.5 Redis Pub/Sub
- [ ] สร้าง `simulator/publisher.py`
- [ ] Publish AGV position ทุก 500ms ไปที่ Redis channel `agv:positions`
- [ ] Format: `{"agv_id": 1, "row": 3, "col": 5, "state": "moving", "battery": 87.5}`

### 3.6 WebSocket Endpoint
- [ ] เพิ่ม `app/routers/ws.py`
- [ ] `WS /ws/agv` — subscribe Redis channel แล้ว broadcast ให้ frontend
- [ ] Connection manager: track clients ที่ connect อยู่
- [ ] Auto-reconnect handling

### 3.7 AGV Log
- [ ] บันทึกทุก movement ลง `agv_logs` table
- [ ] `GET /agvs/{id}/logs` — ดู history ของ AGV ตัวนั้น
- [ ] `GET /agvs/logs` — ดู log ทั้งหมด (filter by date)

### 3.8 เพิ่ม simulator service ใน Docker Compose
- [ ] สร้าง `simulator/Dockerfile`
- [ ] เพิ่ม service `simulator` ใน docker-compose.yml
- [ ] depends_on: backend, redis, postgres

**Deliverable:** รัน AGV 3 ตัวพร้อมกัน, position อัปเดตผ่าน WebSocket ได้จริง

---

## Phase 4 — Frontend Dashboard
> สัปดาห์ 7–10 (parallel กับ Phase 3) | สถานะ: ⬜ ยังไม่เริ่ม

### 4.1 Setup
- [ ] `cd frontend && npm create vite@latest . -- --template react-ts`
- [ ] ลง dependencies: `tailwindcss shadcn-ui zustand react-router-dom axios socket.io-client`
- [ ] Setup Tailwind config
- [ ] Setup React Router (routes: /, /orders, /inventory, /agvs, /logs)
- [ ] Setup Zustand store (agvStore, orderStore)
- [ ] Setup axios instance ชี้ไปที่ `VITE_API_URL`

### 4.2 Layout & Navigation
- [ ] สร้าง `components/Layout.tsx` — sidebar + topbar
- [ ] Sidebar links: Dashboard, Orders, Inventory, AGV Monitor, Logs
- [ ] Topbar: ชื่อระบบ, สถานะ connection, user badge

### 4.3 Warehouse Map
- [ ] สร้าง `components/WarehouseMap.tsx`
- [ ] Render grid 16×12 ด้วย SVG หรือ Konva.js
- [ ] Color-code แต่ละ zone (shelf/inbound/outbound/charge/aisle)
- [ ] แสดง location code บน shelf cell
- [ ] Highlight cell เมื่อ hover

### 4.4 AGV Overlay (Real-time)
- [ ] สร้าง `components/AGVOverlay.tsx`
- [ ] Connect WebSocket ที่ `/ws/agv`
- [ ] แสดง robot icon บน map ตาม position จริง
- [ ] Color แตกต่างตาม state (idle=gray, moving=green, picking=blue, charging=amber)
- [ ] Battery arc รอบตัว robot
- [ ] Tooltip แสดง AGV name, state, battery, current task
- [ ] Animation เคลื่อนที่ smooth ระหว่าง cell

### 4.5 Dashboard Page (`/`)
- [ ] Stat cards: Orders today, Items picked, AGVs active, Low stock alerts
- [ ] Recent orders table (5 รายการล่าสุด)
- [ ] AGV status mini cards (3 ตัว)
- [ ] Warehouse map พร้อม AGV overlay

### 4.6 Orders Page (`/orders`)
- [ ] ตาราง orders ทั้งหมด + filter by status
- [ ] Status badge (pending/picking/packed/dispatched) พร้อม color
- [ ] Form สร้าง order ใหม่ (เลือกสินค้า + quantity)
- [ ] Order detail modal: แสดง items, pick list, AGV ที่ assigned
- [ ] Timeline แสดง order history

### 4.7 Inventory Page (`/inventory`)
- [ ] ตาราง stock ทั้งหมด (product, location, quantity)
- [ ] Highlight แดงเมื่อ quantity ต่ำ
- [ ] Search/filter by product name หรือ location
- [ ] คลิก row แล้ว highlight location บน warehouse map

### 4.8 AGV Monitor Page (`/agvs`)
- [ ] Warehouse map ขนาดใหญ่พร้อม AGV real-time
- [ ] AGV cards แสดง state, battery, current task
- [ ] Form สร้าง manual task (from, to, priority, assign to)
- [ ] Task queue table

### 4.9 Logs Page (`/logs`)
- [ ] ตาราง AGV movement log ทั้งหมด
- [ ] Filter by AGV, date range
- [ ] Export เป็น CSV

### 4.10 Authentication
- [ ] Login page
- [ ] เก็บ JWT token ใน localStorage
- [ ] Protected routes (redirect ถ้าไม่ได้ login)

**Deliverable:** เปิด browser แล้วเห็น dashboard สมบูรณ์, สร้าง order → เห็น AGV เดินไป pick จริง

---

## Phase 5 — Polish, Deploy & Portfolio
> สัปดาห์ 11–14 | สถานะ: ⬜ ยังไม่เริ่ม

### 5.1 Testing
- [ ] เขียน E2E test ด้วย Playwright
  - [ ] Login flow
  - [ ] Create order → AGV assigned → status complete
  - [ ] WebSocket ได้รับ position update
- [ ] pytest coverage > 70% สำหรับ backend

### 5.2 Deploy Backend (Railway)
- [ ] สมัคร Railway account
- [ ] สร้าง project ใหม่ใน Railway
- [ ] Add service: GitHub repo → backend
- [ ] Add PostgreSQL plugin
- [ ] Add Redis plugin
- [ ] Set environment variables (DATABASE_URL, REDIS_URL, SECRET_KEY)
- [ ] Deploy แล้วทดสอบ `/health` endpoint

### 5.3 Deploy Frontend (Vercel)
- [ ] สมัคร Vercel account
- [ ] Import GitHub repo → frontend folder
- [ ] Set `VITE_API_URL` = Railway backend URL
- [ ] Deploy แล้วทดสอบ live

### 5.4 GitHub Actions CI
- [ ] สร้าง `.github/workflows/ci.yml`
- [ ] Trigger: push to main
- [ ] Jobs: lint (ruff), test (pytest), build frontend

### 5.5 README สมบูรณ์
- [ ] เพิ่ม GIF หรือ video demo (record ด้วย OBS หรือ ShareX)
- [ ] Live URL (Railway + Vercel)
- [ ] Architecture diagram (draw.io หรือ Excalidraw)
- [ ] Tech decisions: อธิบายว่าทำไมถึงเลือก stack นี้
- [ ] API documentation link (Swagger URL)

### 5.6 Demo Script (สำหรับ Interview)
- [ ] เขียน script สาธิต 3 นาที
  1. เปิด dashboard แสดง warehouse map
  2. สร้าง order ใหม่
  3. เห็น AGV รับ task และเดินไป pick
  4. Order status อัปเดต real-time
  5. ดู AGV log history
- [ ] ซ้อมพูดอธิบาย business value ให้ non-tech interviewer เข้าใจได้

**Deliverable:** Live URL พร้อมส่ง recruiter, GitHub repo ดูเป็น professional, demo video แนบ CV ได้

---

## Bonus (ทำเพิ่มถ้ามีเวลา)

- [ ] Multi-AGV collision avoidance (หยุดรอถ้าเส้นทางชน)
- [ ] Dark/Light mode toggle
- [ ] Email notification เมื่อ order complete (SendGrid)
- [ ] Analytics page: throughput per hour, AGV utilization rate
- [ ] Mobile-responsive dashboard

---

## Tech Decisions (สำหรับอธิบาย interviewer)

| ทำไมถึงเลือก | เหตุผล |
|---|---|
| FastAPI | async native, auto Swagger docs, Python ecosystem เหมาะกับ logistics |
| PostgreSQL | relational data เหมาะกับ order/inventory, ACID compliance |
| Redis | low-latency pub/sub สำหรับ real-time AGV position |
| asyncio | จำลอง AGV หลายตัวพร้อมกันโดยไม่ต้องใช้ thread |
| Docker Compose | reproducible environment, recruiter รัน demo ได้ทันที |
| Railway | free tier พอสำหรับ portfolio, deploy ง่ายผ่าน Git |

---

*อัปเดตล่าสุด: April 2026*
