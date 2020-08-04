from google.cloud import vision
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    './vision-api-dev-283300-2b166543073f.json'
)
client = vision.ImageAnnotatorClient(credentials=credentials)

response = client.text_detection(image="https://valmore.work/wp-content/uploads/2019/10/load-sign.jpg")

for text in response.text_annotations:
    print(text.description)
# response = client.annotate_image({
#     'image': {'source': {'image_uri': 'https://image.news.livedoor.com/newsimage/stf/1/0/101a2_1581_8c61308dc67bdde67f4ecd8f78c48407.jpg'}},
#     'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}],
# })

print(response)
# for face in response.annotations[0].faces:
#     print(face.joy)

# for logo in response.annotations[0].logos:
#     print(logo.description)
