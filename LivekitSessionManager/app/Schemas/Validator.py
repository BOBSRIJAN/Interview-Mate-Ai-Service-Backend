from pydantic import BaseModel

class UserSessionRequest(BaseModel):
    userid: str
    topics: list[str] | None = None
    paragraph: str | None = None
    duration: int  


class UserSessionResponce(BaseModel):
    roomname: str
    token: str
    livekiturl: str
    

class AgentSessionRequest(BaseModel):
    roomname: str


class AgentSessionResponce(BaseModel):
    roomname: str
    token: str
    livekiturl: str