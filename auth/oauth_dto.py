from pydantic import BaseModel

class OAuthVerifyRequest(BaseModel):
    id_token: str

class UserInfoResponse(BaseModel):
    user_id: int
    email: str
    nickname: str
    oauth_id: str