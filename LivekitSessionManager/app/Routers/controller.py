
from app.Components.AgentSession import createAgentSession
from app.Components.UserSession import createUserSession
from app.BrokerUnit.brokerMethods import BrokerMethods
# from app.CacheUnit.cacheMethods import // nees to create that class, I will work tommorrow on that
from app.Schemas.Validator import (
    UserSessionRequest,  UserSessionResponce, 
    AgentSessionResponce, AgentSessionRequest
)
from app.Config.envConfig import Envar

states: dict = {} 

class Workers:
    pass
    