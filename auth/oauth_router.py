from fastapi import APIRouter
from oauth_service import OAuthService
from oauth_dto import OAuthVerifyRequest

router = APIRouter(
    prefix="/oauth",
)

@router.post("/verify")
async def oauth_login(request: OAuthVerifyRequest):
    oauth_service = OAuthService()
    return await oauth_service.login(request)
