import boto3
import io
from PIL import Image

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')


def make_binary(image_path):
    image = Image.open(image_path)
    stream = io.BytesIO()
    image.save(stream, format="JPEG")
    image_binary = stream.getvalue()
    return image_binary

def create_response(image_binary):
    response = rekognition.search_faces_by_image(
        CollectionId='Accused',
        Image={'Bytes': image_binary}
    )
    found = False
    for match in response['FaceMatches']:
        #print(match['Face']['FaceId'], match['Face']['Confidence'])
        face = dynamodb.get_item(
            TableName='face_regontion',
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
        )
        if 'Item' in face:
            print("Found Offender: ", face['Item']['FullName']['S'])
            found = True
            return "This is : " + face['Item']['FullName']['S'] + " Stay Safe...."

    if not found:
        return "This person is not a offender"