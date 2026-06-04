
from redis import Redis
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger("uvicorn")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

async def initRedis() -> Redis:
    logger.info("Initializing Redis Module.")
    
    try:
        redis: Redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True) 
        
        if not redis:
            logger.error("System does not Initializing the Redis.")
            return
        
        logger.info("Radis Initializations Done.")
        return redis
    
    except Exception as e: 
        logger.exception(f"Redis from CacheUnit file: {e}")