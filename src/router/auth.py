import requests
from fastapi import APIRouter

auth_router = APIRouter(
    tags=["Auth"],
)


@auth_router.get("/login/kakao")
def kakao_login(code: str):
    """
    https://kauth.kakao.com/oauth/authorize?client_id=d12d5a49f7a6ae9c1fb44443ec2f18fb&redirect_uri=http://localhost:8000/api/v1/auth/login/kakao&response_type=code
    위의 URL로 접속한 다음에, 이루어지는 로직
    """
    # 토큰 발급
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

    # 액세스 토큰으로 부터 유저 정보 조회
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

    response_dict.get("email")
    response_dict.get("profile").get("nickname")
    response_dict.get("profile").get("thumbnail_image_url")
