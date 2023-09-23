import requests
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from src.auth.auth import generate_access_token
from src.user.application.user import UserService
from src.user.repository.users import UserRepository

auth_router = APIRouter(
    tags=["Auth"],
)


@auth_router.get("/login/kakao")
async def kakao_login(code: str, session: AsyncSession = Depends(get_session)):
    """
    https://kauth.kakao.com/oauth/authorize?client_id=d12d5a49f7a6ae9c1fb44443ec2f18fb&redirect_uri=http://localhost:8000/api/v1/auth/login/kakao&response_type=code
    위의 URL로 접속한 다음에, 이루어지는 로직
    """
    # TODO: 해당 함수 리펙토링 하기
    """
    문제점이라고 생각되는 것들
    1. 페이로드가 좀 더럽다?
    2. 함수 하나가 너무 길다.
    3.
    """
    # STEP 1. 토큰 발급
    url = "https://kauth.kakao.com/oauth/token"
    kakao_data = {
        "grant_type": "authorization_code",
        "client_id": "d12d5a49f7a6ae9c1fb44443ec2f18fb",
        "redirect_uri": "http://localhost:8000/api/v1/auth/login/kakao",
        "code": code,
        "client_secret": "Xh89YsF1r4D3BnrzcM7hHSluF7TrkIxz",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    response = requests.post(url, data=kakao_data, headers=headers)
    access_token_dict = response.json()
    access_token = access_token_dict["access_token"]

    # STEP 2. 액세스 토큰으로 부터 유저 정보 조회
    headers = {
        "Content-Type": "Content-type: application/x-www-form-urlencoded;charset=utf-8",
        "Authorization": f"Bearer {access_token}",
    }
    data = {
        "property_keys": '["kakao_account.email", "kakao_account.profile, "kakao_account.name"]'
    }

    url = "https://kapi.kakao.com/v2/user/me"
    response = requests.post(url, headers=headers, data=data)
    response_dict = response.json().get("kakao_account")

    email = response_dict.get("email")
    nickname = response_dict.get("profile").get("nickname")
    response_dict.get("profile").get("thumbnail_image_url")

    # STEP 3. 이메일을 조회한다.
    # 유저 이메일을 조회했을 때 회원이 존재한다면, 회원가입 아니면 액세스 토큰을 만들어서 반환
    user_service = UserService(user_repository=UserRepository(session=session))
    user = await user_service.get_user_by_email(email=email)
    # 유저가 존재하면, 액세스 토큰을 만들어서 전달한다.
    # TODO: 3. 여기 로직을 개선할 수 있을 것 같다. 4. 토큰값을 리턴해야하는데 현재 그냥 "test" 문자열 리턴하고 있음

    if user:
        return await generate_access_token(email=email)
    else:
        # 유저가 존재하지 않으면 회원 가입 및 생성 및 토큰을 전달한다.
        user = await user_service.create_user(nickname=nickname, email=email)
        response = await generate_access_token(email=email)
        await session.commit()
        return "test"
