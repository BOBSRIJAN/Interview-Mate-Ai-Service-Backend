
from redis.asyncio import Redis
import logging

logger = logging.getLogger("uvicorn")

class cacheMethods:
    
    @staticmethod
    async def shutdownRadis(states: dict) -> None: 
        redisClient: Redis = states.get("Redis")
        
        if redisClient:
            logger.info("Redis Cache Unit Shutdown Successfully.")
            await redisClient.aclose()