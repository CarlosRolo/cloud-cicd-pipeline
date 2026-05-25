from fastapi import FastAPI
from app.routers import health, items

app = FastAPI(
    title="CLOUD-03 CI/CD Pipeline API",
    description="FastAPI with full CI/CD pipeline via GitHub Actions",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(items.router)
