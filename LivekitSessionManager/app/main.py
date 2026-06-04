
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.Routers.route import AppRouter
from app.Routers.controller import states
from app.CacheUnit.RedisConfig import initRedis
from dotenv import load_dotenv
from fastapi import FastAPI
import asyncio
import logging
import os

load_dotenv()

logger = logging.getLogger("uvicorn")

async def banner() -> None:
    with open(r"app/resources/banner.txt", "r", encoding="utf-8") as file:
        content = file.read()
    logger.info(f"\n{content}\n")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await banner()
    states["Redis"] = await initRedis()
    yield
    
app: FastAPI = FastAPI(title="Live-kit-session-manager", lifespan=lifespan)

GLOBAL_HOST: str = os.getenv('GLOBAL_HOST')
ALLOWHOST = ["http://localhost:5173", "http://127.0.0.1:5173", GLOBAL_HOST]

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