import json

class KeyLoad:
    def __init__(self):
        with open("./secretKey.json", 'r') as file:
            data = json.load(file)
            self.__paymentKey = data["paymentkey"]
            self.__kakaokey = data["kakaoKey"]
            self.__secretKey = data["secretKey"]
            
    def getPeymentKey(self):
        return self.__paymentKey
    
    def getSecretKey(self):
        return self.__secretKey
        
    def getKakaoKey(self):
        return self.__kakaoKey