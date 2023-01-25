import requests
import json

class KakaoLogin:
    def __init__(self):
        self.__cilentKey = "Client Key"
        self.__restAPI = "RestApi Key"
    def getToken(self,token):
        url = "https://kapi.kakao.com/v1/user/me"

        headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control':"no-cache"
                }

        headers.update({'Authorization':"Bearer"+str(token)})
        res = requests.request("POST",url,headers=headers)

        return(res.text)
