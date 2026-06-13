
from app.Schemas.Validator import SystemStatusResponce
from app.Routers.controller import apiController
from fastapi import APIRouter, status
import logging


logger = logging.getLogger("uvicorn")

AppRouter: APIRouter = APIRouter(prefix="/api/v1/livekitsessionmanager", tags=["systemstatus"])

@AppRouter.get("/systemstatus", response_model=SystemStatusResponce, status_code=status.HTTP_200_OK)
async def systemStatus() -> SystemStatusResponce:
    return await apiController._systemstatus()