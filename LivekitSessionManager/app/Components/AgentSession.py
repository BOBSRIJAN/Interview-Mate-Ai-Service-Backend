
from app.Schemas.Validator import UserSessionResponce, AgentSessionResponce
from livekit.api import AccessToken, VideoGrants
from app.Config.envConfig import Envar
import uuid


async def createAgentSession(req: UserSessionResponce) -> AgentSessionResponce:
    agentIdentity: str = f"agent-{uuid.uuid4()}"
    roomname: str = req.roomname

    token: str = (
        AccessToken(Envar.LIVEKIT_API_KEY, Envar.LIVEKIT_API_SECRET)
        .with_identity(agentIdentity)
        .with_name("Agent")
        .with_grants(
            VideoGrants(
                room_join=True,
                room=roomname,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .to_jwt()
    )

    return {
        "roomname": roomname,
        "token": token,
        "livekiturl": Envar.LIVEKIT_URL,
    }