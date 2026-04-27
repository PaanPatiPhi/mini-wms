# Mini WMS — Project Plan

> ระบบจำลอง Warehouse Management System พร้อม Mock AGV สำหรับ Portfolio

**Stack:** FastAPI · PostgreSQL · Redis · React · TypeScript · Docker  
**Deploy:** Railway (backend) · Vercel (frontend)  
**ระยะเวลารวม:** ~10–14 สัปดาห์

---

## Branch Strategy

```
main     — stable, deploy ได้เสมอ
dev      — รวม feature ที่เสร็จแล้ว
feature/ — แตกจาก dev ทำทีละ phase
```

---

## Phase 1 — Foundation & Data Model
> สถานะ: ✅ เสร็จแล้ว | merge เข้า main แล้ว

- [x] Docker Compose: postgres + redis + backend
- [x] Dockerfile สำหรับ backend (python:3.12-slim)
- [x] Database Schema: 8 tables
- [x] Alembic migration: initial tables
- [x] Seed data: products 10 รายการ, locations, inventory, AGV 3 ตัว
- [x] README เบื้องต้น

---

## Phase 2 — Core WMS API
> สถานะ: ✅ เสร็จแล้ว | merge เข้า dev แล้ว

- [x] Schemas (Pydantic v2 ConfigDict): product, location, inventory, order, agv, task, user
- [x] Inventory API: GET all, GET by id, GET low-stock, PUT quantity
- [x] Order API: POST create (stock check), GET all/filter, GET by id, PATCH status flow
- [x] AGV API: GET all, GET by id, PATCH state
- [x] Task API: POST create (auto-assign), GET all/filter, GET by id, PATCH status
- [x] Location API: GET all, GET by id (เพิ่มระหว่าง Phase 3)
- [x] Register routers ใน main.py (/api/v1/ prefix)
- [x] JWT Auth: register, login, get_current_user, get_admin_user
- [x] Unit tests (pytest): 7/7 passed
- [x] Fix Pydantic v2 warnings (ConfigDict)

---

## Phase 3 — AGV Simulator + Real-time
> สถานะ: ✅ เสร็จแล้ว | Branch: feature/phase3-agv-simulator

- [x] simulator/grid.py — warehouse grid 12×16, cell types, is_walkable(), get_neighbors()
- [x] simulator/pathfinder.py — BFS algorithm, obstacle avoidance, fallback
- [x] simulator/agv_agent.py — state machine (idle→moving→picking→delivering→idle), battery drain, auto-dock, httpx API calls
- [x] simulator/dispatcher.py — poll tasks ทุก 2 วินาที, priority sort, auto-assign, follow_redirects
- [x] simulator/publisher.py — Redis Pub/Sub broadcast ทุก 500ms
- [x] simulator/main.py — asyncio.gather(), load AGVs from DB
- [x] backend/app/routers/ws.py — WebSocket /ws/agv, ConnectionManager, Redis subscribe
- [x] Bug fix: update_state_in_db(DELIVER_DELAY) → update_state_in_db(IDLE)
- [x] Bug fix: fetch locations จาก /locations/ แทน /inventory/
- [x] Bug fix: follow_redirects=True ทุก httpx call

**Deliverable:** ✅ AGV 3 ตัวรันพร้อมกัน, tasks done ครบ, state กลับ idle สมบูรณ์

---

## Phase 4 — Frontend Dashboard
> สถานะ: 🟡 กำลังทำ | Branch: feature/phase4-frontend

### 4.1 Setup
- [ ] npm create vite@latest . -- --template react-ts
- [ ] ลง: tailwindcss, shadcn/ui, zustand, react-router-dom, axios, socket.io-client
- [ ] Setup Tailwind config
- [ ] React Router: /, /orders, /inventory, /agvs, /logs
- [ ] Zustand store: agvStore, orderStore
- [ ] axios instance ชี้ไปที่ VITE_API_URL

### 4.2 Layout & Navigation
- [ ] components/Layout.tsx — sidebar + topbar
- [ ] Sidebar: Dashboard, Orders, Inventory, AGV Monitor, Logs

### 4.3 Warehouse Map
- [ ] components/WarehouseMap.tsx
- [ ] SVG grid 16×12, color-code zones
- [ ] แสดง location code บน shelf cell

### 4.4 AGV Overlay (Real-time)
- [ ] components/AGVOverlay.tsx
- [ ] WebSocket connect /ws/agv
- [ ] Robot icon ตาม position จริง
- [ ] Color ตาม state, battery arc, tooltip
- [ ] Animation smooth

### 4.5 Dashboard Page (/)
- [ ] Stat cards: Orders today, Items picked, AGVs active, Low stock
- [ ] Recent orders table
- [ ] Warehouse map + AGV overlay

### 4.6 Orders Page (/orders)
- [ ] ตาราง + filter by status
- [ ] Form สร้าง order ใหม่
- [ ] Order detail modal

### 4.7 Inventory Page (/inventory)
- [ ] ตาราง stock, highlight low stock, search/filter

### 4.8 AGV Monitor Page (/agvs)
- [ ] Map ขนาดใหญ่ + AGV real-time
- [ ] AGV cards: state, battery, task
- [ ] Form สร้าง manual task

### 4.9 Logs Page (/logs)
- [ ] AGV movement log, filter, export CSV

### 4.10 Authentication
- [ ] Login page, JWT localStorage, protected routes

**Deliverable:** Dashboard สมบูรณ์, สร้าง order → เห็น AGV เดินไป pick real-time

---

## Phase 5 — Polish, Deploy & Portfolio
> สถานะ: ⬜ ยังไม่เริ่ม

### 5.1 Testing
- [ ] E2E Playwright: login, create order, AGV assigned, WebSocket
- [ ] pytest coverage > 70%

### 5.2 Deploy Backend (Railway)
- [ ] PostgreSQL + Redis plugin, environment variables

### 5.3 Deploy Frontend (Vercel)
- [ ] VITE_API_URL = Railway URL

### 5.4 GitHub Actions CI
- [ ] lint + pytest + build on push to main

### 5.5 README สมบูรณ์
- [ ] GIF/video demo, live URL, architecture diagram, tech decisions

### 5.6 Demo Script (Interview)
- [ ] Script 3 นาที, อธิบาย business value ให้ non-tech เข้าใจ

**Deliverable:** Live URL พร้อมส่ง recruiter, demo video แนบ CV

---

## Bonus

- [ ] Multi-AGV collision avoidance
- [ ] VDA5050 protocol (MQTT)
- [ ] Analytics page: throughput, AGV utilization
- [ ] Mobile-responsive
- [ ] Email notification (SendGrid)

---

## Tech Decisions

| เลือก | เหตุผล |
|---|---|
| FastAPI | async native, auto Swagger, Python เหมาะกับ logistics |
| PostgreSQL | relational, ACID compliance |
| Redis | low-latency pub/sub สำหรับ real-time |
| asyncio | AGV หลายตัวพร้อมกันโดยไม่ต้องใช้ thread |
| Docker Compose | reproducible, recruiter รัน demo ได้ทันที |
| Railway | free tier, deploy ง่าย |
| BFS Pathfinding | เส้นทางสั้นที่สุด, ต่อยอดเป็น A* ได้ |

---

## Project Structure

```
mini-wms/
├── backend/
│   ├── app/
│   │   ├── core/         # security, dependencies
│   │   ├── models/       # SQLAlchemy tables
│   │   ├── routers/      # API endpoints + WebSocket
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── database.py
│   │   ├── main.py
│   │   └── seed.py
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── simulator/
│   ├── grid.py
│   ├── pathfinder.py
│   ├── agv_agent.py
│   ├── dispatcher.py
│   ├── publisher.py
│   └── main.py
├── frontend/             (Phase 4)
├── docker-compose.yml
├── PLAN.md
└── README.md
```

---

*อัปเดตล่าสุด: April 2026 — Phase 1 ✅ Phase 2 ✅ Phase 3 ✅ Phase 4 🟡*
