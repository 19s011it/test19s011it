from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os

app=Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN="25lpFw9LMOCSpo4SJLlTFjC2Kzvk/u2Dla62dAxnQLd3WR86h0DDHtRefVGHcTra6JSajtHPE/EBMdlX3SyspYwFxsQZHr9FCQj8Mzc5FT7HozOjQIuxjt+AN9PJ0MISqjvXUAFHTMZ7yOoRqGi3rgdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET="ccc5b73b57b83105d02aeb5deaeb556f"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
