from flask import Flask, request,abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import  MessageEvent,TextMessage, TextSendMessage, ImageSendMessage, ImageMessage
import os
from google.cloud import vision
from google.oauth2 import service_account

app=Flask(__name__)

#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
URL = "https://test19s011it.herokuapp.com/static/"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    print("Request body: {}".format(body))
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"
 
#テキストの場合
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
#画像の場合
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    #print ("[NATTO]: {}".format(event))
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
 
#画像を保存する
    with open("static/" + message_id + ".jpg", "wb") as f:
        f.write(message_content.content)

    credentials = service_account.Credentials.from_service_account_file(
        './vision-api-dev-283300-2b166543073f.json'
    )
    client = vision.ImageAnnotatorClient(credentials=credentials)
    response = client.text_detection(image=URL + "{}.jpg".format(message_id))
    print(response)

#画像を表示する
    image_url = URL + "{}.jpg".format(message_id)
    image_message = ImageSendMessage(
        original_content_url=image_url,     #開く前の画像
        preview_image_url=image_url,        #開いた時の画像
    )
    line_bot_api.reply_message(event.reply_token, image_message)
 
if __name__=="__main__":
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)