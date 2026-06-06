
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.Routers.route import AppRouter
from app.Routers.controller import states
from app.CacheUnit.cacheConfig import CacheConf
from app.BrokerUnit.brokerConfig import BrokerConf
from app.Config.envConfig import Envar
from app.Config.envConfig import Envar
from dotenv import load_dotenv
from fastapi import FastAPI
import asyncio
import logging

load_dotenv()

logger = logging.getLogger("uvicorn")

async def banner() -> None:
    with open(r"app/Resources/banner.txt", "r", encoding="utf-8") as file:
        content = file.read()
    logger.info(f"\n{content}\n")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await banner()
    states["Redis"] = await CacheConf.initRedis()
    states['KafkaConsumer'] = await BrokerConf.initKafkaConsumer()
    states['KafkaProducer'] = await BrokerConf.initKafkaProducer()
    
    yield
    

app: FastAPI = FastAPI(title="Livekit-session-manager", lifespan=lifespan, docs_url=None, redoc_url=None)

GLOBAL_HOST: str = Envar.GLOBAL_HOST
ALLOWHOST = ["http://localhost:5173", GLOBAL_HOST]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWHOST,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(AppRouter)

@app.get("/")
def root():
    return {"message": "Welcome To SRIJAN'S Backend Server!"}