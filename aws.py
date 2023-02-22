# -*- coding: utf-8 -*-
import boto3
from keyLoad import KeyLoad

class MufiS3:
    def __init__(self):
        key =KeyLoad()
        AWS_ACCESS_KEY_ID = key.getAwsKey()
        AWS_SECRET_ACCESS_KEY = key.getAwsSecretKey()
        AWS_DEFAULT_REGION = key.getAwsRegion()
        session = boto3.Session(
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_DEFAULT_REGION)
        self.__s3 = session.resource('s3')
        
    def uploadImage(self, image, imageName):
        file = image.read()
        bucket = 'mufi-photo'
        key = 'kiosk-photo/'+imageName+'.png'
        
        self.__s3.Object(bucket, key).put(Body=file)
        
        return 1