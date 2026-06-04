
from fastapi import APIRouter, status
from dotenv import load_dotenv
import logging
import psutil
import os

load_dotenv()

logger = logging.getLogger("uvicorn")

AppRouter: APIRouter = APIRouter(prefix="/livekitsessionmanager", tags=["systemstatus"])

@AppRouter.get("/systemstatus", response_model=dict, status_code=status.HTTP_200_OK)
async def systemStatus() -> dict:
    process = psutil.Process(os.getpid())
    return {
        "cpupercent": process.cpu_percent(),
        "memorymb": process.memory_info().rss / 1024 / 1024,
        "threads": process.num_threads()
    }