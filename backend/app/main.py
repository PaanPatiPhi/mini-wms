from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.routers import inventory, orders, agvs, tasks, auth, ws, location

app = FastAPI(title="Mini WMS", version="0.1.0", description="Warehouse Management System with Mock AGV")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(agvs.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(ws.router)
app.include_router(location.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Mini WMS is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}