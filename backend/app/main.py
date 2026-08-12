from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import analysis

app = FastAPI(
    title="Research Report Assistant API",
    description="API untuk analisis statistik otomatis dari file CSV/Excel",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "research-report-assistant-api"}
