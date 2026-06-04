
from livekit.api import AccessToken, VideoGrants
from app.Schemas.DataExchangeModel import SessionRequest, SessionResponce
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

states: dict = {} 

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")


async def createSession(res: SessionRequest) -> SessionResponce:
    roomName: str = f"Imate-room-{uuid.uuid4()}"
    userIdentity: str = res.userid

    token: str = (
        AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(userIdentity)
        .with_name(res.userid)
        .with_grants(
            VideoGrants(
                room_join=True,
                room=roomName,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .to_jwt()
    )
    
    return {
        "roomname": roomName,
        "token": token,
        "livekiturl": LIVEKIT_URL,
    }