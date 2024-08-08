from flask import Flask, request, abort
from flask import render_template

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage         # 傳輸回Line官方後台的資料格式
)
from linebot.v3.webhooks import (
    MessageEvent,       # 傳輸過來的方法
    TextMessageContent  # 使用者傳過來的資料格式
)
import os, sys

app = Flask(__name__)

# 從環境變數取得 secret key & access token
channel_secret = os.getenv('LINEBOT_SECRET_KEY', None)
channel_access_token = os.getenv('LINEBOT_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINEBOT_SECRET_KEY as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINEBOT_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


# 設計一個callback的路由，用來提供給Line的官方後台去呼叫
# 也就是所謂的Webhook Server
# 官方會將使用者傳的訊息轉傳給Webhook Server
# 所以會使用 RESTful API 的 POST 方法
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 測試用，確定 webhook server 有連通
@app.route("/")
def say_hello(username=None):
    return render_template("hello.html",name=username)

# 根據不同的使用者事件(Event)，用不同的方式回應
# eg. MessageEvent 代表使用者傳輸訊息(包含 純文字、圖片、聲音、貼圖...)
# TextMessageContent 代表使用者傳輸的訊息內容是文字
# 符合兩者條件的事件會被handler_message 所處理
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    
    app.run(debug=True)  # debug=True 程式碼更動後直接更新到網頁上，不用重新執行 python xxxx.py