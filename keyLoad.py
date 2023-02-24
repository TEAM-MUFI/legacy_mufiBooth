import json

class KeyLoad:
    def __init__(self):
        with open("./secretKey.json", 'r') as file:
            data = json.load(file)
            self.__paymentKey = data["paymentkey"]
            self.__kakaoRestAPIkey = data["kakaoRestAPIKey"]
            self.__secretKey = data["secretKey"]
            self.__awsAccessKey = data["AWS_ACCESS_KEY"]
            self.__awsSecretAccessKey = data["AWS_SECRET_ACCESS_KEY"]
            self.__awsRegion = data["AWS_DEFAULT_REGION"]
            
    def getPeymentKey(self):
        return self.__paymentKey
    
    def getSecretKey(self):
        return self.__secretKey
        
    def getKakaoRestAPIKey(self):
        return self.__kakaoRestAPIkey
        
    def getAwsKey(self):
        return self.__awsAccessKey
        
    def getAwsSecretKey(self):
        return self.__awsSecretAccessKey
        
    def getAwsRegion(self):
        return self.__awsRegion