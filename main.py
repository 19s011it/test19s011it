from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage
import os

app=Flask(__name__)

#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN=os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET=os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

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

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,messages=make_image_message())

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

def make_image_message(event):
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    with open(Path(f"static/images/{message_id}.jpg").absolute(), "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    main_image_path = f"static/images/{message_id}_main.jpg"
    preview_image_path = f"static/images/{message_id}_preview.jpg"

    messages = ImageSendMessage(
        original_content_url=f"https://date-the-image.herokuapp.com/{main_image_path}",
        preview_image_url=f"https://date-the-image.herokuapp.com/{preview_image_path}",
    )
    line_bot_api.reply_message(event.reply_token, messages )
#    messages = ImageSendMessage(
#        original_content_url="https://upload.wikimedia.org/wikipedia/commons/0/0a/Kagoshima_Career_Design_College.JPG",
#        preview_image_url="https://hogehoge-mini.jpg"
#    )
    return messages

if __name__=="__main__":
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
