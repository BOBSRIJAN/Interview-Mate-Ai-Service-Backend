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
    

class SystemStatusResponce(BaseModel): 
    cpupercent: int | float
    memorymb: int | float
    threads: int 


class CurrentUserSessionRequest(BaseModel):
    userid: str | int


class CurrentUserSessionResponce(BaseModel):
    userid: str | None
    topics: list[str] | None = None
    paragraph: str | None = None
    duration: int | None
    roomname: str | None
    token: str | None
    livekiturl: str | None