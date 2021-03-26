from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('LvEQ5TUWhqMHjrgoppECy80KBIQIGJciGwPgrn2V3wybvr5CzE31z5kX8Hx6rXsybBGcORHPxk3FcM0zyhBKGsrwtitlS+IscmydV+ILN7AxxluiIOoaH3t0CBHXpvxVzaQIS3fVEpqjGwCyCybEBAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('35adbbf06a176397589e33cd294ee0fa')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '說說別的吧'
    if msg in ['hi', 'Hi']:
        r = '哈囉~'
    elif msg == '陪我聊天':
        r = '來吧~'
    elif msg in ['難過', '傷心', '嗚嗚']:
        r = '笑一個吧^_<'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()