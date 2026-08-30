
from infra.priority_db import RefreshToken
from oauth_dto import UserInfoResponse
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

class JWTService:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def create_access_token(self, user_info: UserInfoResponse, expire_delta: int = 3600):
        payload = {
            "user_id": user_info.user_id
        }
        payload["exp"] = jwt.datetime.datetime.utcnow() + jwt.timedelta(seconds=expire_delta)
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    async def create_access_and_refresh(self, user_info: UserInfoResponse, access_expire_delta: int = 3600, refresh_expire_delta: int = 604800, db: AsyncSession = None):
        access_token = self.create_access_token(user_info, access_expire_delta)
        refresh_payload = {
            "user_id": user_info.user_id
        }
        refresh_payload["exp"] = jwt.datetime.datetime.utcnow() + jwt.timedelta(seconds=refresh_expire_delta)
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        db.add(RefreshToken(user_id=user_info.user_id, token=refresh_token))
        await db.commit()

        return access_token, refresh_token


    async def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

