
from app.Schemas.Validator import UserSessionRequest, UserSessionResponce
from livekit.api import AccessToken, VideoGrants
from app.Config.envConfig import Envar
import uuid


async def createUserSession(req: UserSessionRequest) -> UserSessionResponce:
    roomName: str = f"Imate-room-{uuid.uuid4()}"
    userIdentity: str = req.userid

    token: str = (
        AccessToken(Envar.LIVEKIT_API_KEY, Envar.LIVEKIT_API_SECRET)
        .with_identity(userIdentity)
        .with_name(req.userid)
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
        "livekiturl": Envar.LIVEKIT_URL,
    }