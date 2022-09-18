import requests
import json

class KakaoLogin:
    def __init__(self):
        __cilentKey = "XPCEd81wBQrZdvGLO0AEdmiq8rCAxzg7"
        __restAPI = "1c3149990da4b10646de8c6dbd0bbbe1"
    def getToken(self,code):
        url2 = "https://kauth.kakao.com/oauth/token"

        payload = "grant_type=authorization_code&client_id="+__restAPI+"&redirect_uri=http%3A%2F%2Flocalhost%3A5001&code="+code

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control':"no-cache"
        }

        res = requests.request("POST",url2,data=payload,headers=headers)
        access_token = json.loads(((res.text).encode('utf-8')))['access_token']
        url = "https://kapi.kakao.com/v1/user/signup"

        headers.update({'Authorization':"Bearer"+str(access_token)})
        res = requests.request("POST",url,headers=headers)

        return (res.text)
