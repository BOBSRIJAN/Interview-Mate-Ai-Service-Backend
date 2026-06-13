
from app.BrokerUnit.brokerMethods import BrokerMethods
from app.CacheUnit.cacheMethods import cacheMethods
from fastapi.middleware.cors import CORSMiddleware
from app.BrokerUnit.brokerConfig import BrokerConf
from app.CacheUnit.cacheConfig import CacheConf
from app.Services.Worker import Workers
from contextlib import asynccontextmanager
from app.Services.Worker import states
from app.Routers.route import AppRouter
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
    states['Redis'] = await CacheConf.initRedis()
    states['KafkaConsumerUser'] = await BrokerConf.initKafkaConsumerForUser()
    states['KafkaConsumerAgent'] = await BrokerConf.initKafkaConsumerForAgent()
    states['KafkaProducer'] = await BrokerConf.initKafkaProducer()
    userWorker = asyncio.create_task(Workers.userWorker())
    agentWorker = asyncio.create_task(Workers.agentWorker())

    yield

    userWorker.cancel()
    agentWorker.cancel()
    await BrokerMethods.shutdownConsumer(states=states)
    await BrokerMethods.shutdownProducer(states=states)
    await cacheMethods.shutdownRadis(states=states)


app: FastAPI = FastAPI(
    title="Livekit-Session-Manager", 
    lifespan=lifespan, 
    docs_url=None, 
    redoc_url=None
)

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