import boto3

s3 = boto3.resource('s3')

def upload_user_S3(image):
    file = open(image,'rb')
    object = s3.Object('suspectimages', image)
    ret = object.put(Body=file)
