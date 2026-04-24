from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Mini WMS", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Mini WMS is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}