# Mini WMS — Warehouse Management System

ระบบจำลอง Warehouse Management System พร้อม Mock AGV  
สร้างเพื่อ Portfolio แสดงทักษะ Backend + Real-time Systems

## Tech Stack
- **Backend:** FastAPI, PostgreSQL, Redis, SQLAlchemy
- **Frontend:** React, TypeScript, Tailwind CSS _(coming soon)_
- **Infrastructure:** Docker Compose, Railway, Vercel

## Local Setup

1. Clone repo
```bash
   git clone https://github.com/YOUR_USERNAME/mini-wms.git
   cd mini-wms
```

2. Start all services
```bash
   docker compose up --build
```

3. Seed database
```bash
   docker compose exec backend python -m app.seed
```

4. Open browser
   - API docs: http://localhost:8000/docs

## Project Structure

mini-wms/
├── backend/
│   ├── app/
│   │   ├── models/       # Database tables
│   │   ├── routers/      # API endpoints
│   │   ├── schemas/      # Request/Response types
│   │   ├── database.py   # DB connection
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # DB migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # React app (coming soon)
└── docker-compose.yml

## Status
- [x] Phase 1 — Foundation & Data Model
- [ ] Phase 2 — Core WMS API
- [ ] Phase 3 — AGV Simulator + Real-time
- [ ] Phase 4 — Frontend Dashboard
- [ ] Phase 5 — Deploy & Polish