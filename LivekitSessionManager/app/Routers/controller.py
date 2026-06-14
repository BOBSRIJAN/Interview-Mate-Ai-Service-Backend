
from app.Services.Worker import states
from redis.asyncio import Redis
from app.Schemas.Validator import (
    SystemStatusResponce,
    CurrentUserSessionRequest,
    CurrentUserSessionResponce,
)
from fastapi import (
    status,
    HTTPException,
)
import logging
import psutil
import json
import os

logger = logging.getLogger("uvicorn")


class apiController:

    @staticmethod
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


    @staticmethod
    async def _currentusersession(req: CurrentUserSessionRequest) -> CurrentUserSessionResponce:
        redis: Redis = states.get('Redis')

        try:
            res = await redis.get(str(req.userid))

            if not res:
                raise HTTPException(
                    status_code=404,
                    detail=f"User Data Not Found {req.userid}"
                )

            data = json.loads(res)

            return CurrentUserSessionResponce.model_validate(data)

        except Exception as e:
            logger.exception(f"Unexpected Exception:{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))