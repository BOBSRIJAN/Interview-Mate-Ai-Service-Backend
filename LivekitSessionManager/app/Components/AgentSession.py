
from app.Schemas.Validator import AgentSessionRequest, AgentSessionResponce
from livekit.api import AccessToken, VideoGrants
from app.Config.envConfig import Envar
import uuid


async def createAgentSession(res: AgentSessionRequest) -> AgentSessionResponce:
    agentIdentity = f"agent-{uuid.uuid4()}"
    roomname: str = res.roomname

    token = (
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