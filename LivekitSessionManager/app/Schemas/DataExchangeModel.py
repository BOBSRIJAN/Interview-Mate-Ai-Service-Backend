from pydantic import BaseModel

class SessionRequest(BaseModel):
    userid: str
    topics: list[str] | None = None
    paragraph: str | None = None
    duration: int  


class SessionResponce(BaseModel):
    roomname: str
    token: str
    livekiturl: str

