from fastapi import APIRouter
from app.models.schemas import HealthResponse
import os

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development"),
    )


@router.get("/")
async def root():
    return {"message": "CLOUD-03: CI/CD Pipeline API", "docs": "/docs"}
