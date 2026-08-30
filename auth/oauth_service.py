from oauth_dto import OAuthVerifyRequest
from google.auth.transport import requests
from google.oauth2 import id_token
from infra.priority_db import User
from infra.db_session import db
from oauth_dto import UserInfoResponse
from sqlalchemy.ext.asyncio import AsyncSession

request = requests.Request()

class OAuthService:
    def __init__(self):
        pass

    async def login(self, request: OAuthVerifyRequest, db: AsyncSession):
        try:
            id_info = id_token.verify_oauth2_token(request.id_token, request)
            user_email = id_info.get("email")

            query = await User.query.where(User.email == user_email).gino.first()
            result = db.execute(query)
            if result:
                return UserInfoResponse(
                    user_id=result.id,
                    email=result.email,
                    nickname=result.nickname,
                    oauth_id=result.oauth_id
                )
            else:
                new_user = User(
                    email=user_email,
                    nickname=id_info.get("name"),
                    oauth_id=id_info.get("sub")
                )
                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)

                return UserInfoResponse(
                    user_id=new_user.id,
                    email=new_user.email,
                    nickname=new_user.nickname,
                    oauth_id=new_user.oauth_id
                )
        except ValueError:
            return {"error": "Invalid token"}