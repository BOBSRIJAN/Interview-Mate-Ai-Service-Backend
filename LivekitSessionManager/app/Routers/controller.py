
from app.Schemas.Validator import SystemStatusResponce
from fastapi import HTTPException, status
import logging
import psutil
import os


logger = logging.getLogger("uvicorn")

class apiController:
    async def _systemstatus() -> SystemStatusResponce:
        try: 
            process = psutil.Process(os.getpid())
        except Exception as e:
            logger.exception(f"Faild to get the system ststus: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Faild to get the system ststus: {e}"
            )
        return {
            "cpupercent": psutil.cpu_percent(),
            "memorymb": process.memory_info().rss / 1024 / 1024,
            "threads": process.num_threads()
        }