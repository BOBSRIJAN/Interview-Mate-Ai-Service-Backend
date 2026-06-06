
from app.Config.envConfig import Envar
from redis import Redis
import logging

logger = logging.getLogger("uvicorn")


class CacheConf:

    @staticmethod
    async def initRedis() -> Redis:
        logger.info("Initializing Redis Module.")
        
        try:
            redis: Redis = Redis(host=Envar.REDIS_HOST, port=Envar.REDIS_PORT, decode_responses=True) 
            
            if not redis:
                logger.error("System does not Initializing the Redis.")
                return
            
            logger.info("Radis Initializations Done.")
            return redis
        
        except Exception as e: 
            logger.exception(f"from CacheConfig file: {e}")