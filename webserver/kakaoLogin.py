import requests
import json

class KakaoLogin:
    def __init__(self):
        self.__cilentKey = "XPCEd81wBQrZdvGLO0AEdmiq8rCAxzg7"
        self.__restAPI = "1c3149990da4b10646de8c6dbd0bbbe1"
    def getToken(self,token):
        url = "https://kapi.kakao.com/v1/user/me"

        headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control':"no-cache"
                }

        headers.update({'Authorization':"Bearer"+str(token)})
        res = requests.request("POST",url,headers=headers)

        return(res.text)
