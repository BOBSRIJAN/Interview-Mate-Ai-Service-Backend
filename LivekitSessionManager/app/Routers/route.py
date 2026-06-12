
from fastapi import APIRouter, status, HTTPException
import logging
import psutil
import os


logger = logging.getLogger("uvicorn")

AppRouter: APIRouter = APIRouter(prefix="/api/v1/livekitsessionmanager", tags=["systemstatus"])

@AppRouter.get("/systemstatus", response_model=dict, status_code=status.HTTP_200_OK)
async def systemStatus() -> dict:
    try: 
        process = psutil.Process(os.getpid())
    except Exception as e:
        logger.exception(f"Faild to get the system ststus: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Faild to get the system ststus: {e}")
    return {
        "cpupercent": psutil.cpu_percent(),
        "memorymb": process.memory_info().rss / 1024 / 1024,
        "threads": process.num_threads()
    }