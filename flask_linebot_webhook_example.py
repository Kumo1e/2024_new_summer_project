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
from get_handle_keys import get_secret_and_token
from openai_api import chat_with_gpt

app = Flask(__name__)
keys = get_secret_and_token()
handler = WebhookHandler(keys["LINEBOT_SECRET_KEY"])
configuration = Configuration(access_token=keys["LINEBOT_ACCESS_TOKEN"])
api_key = access_token=keys["OPENAI_API_KEY"]

@app.route("/callback", methods=['POST'])
def callback():
    # 設計一個callback的路由，用來提供給Line的官方後台去呼叫
    # 也就是所謂的Webhook Server
    # 官方會將使用者傳的訊息轉傳給Webhook Server
    # 所以會使用 RESTful API 的 POST 方法
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

@app.route("/")
def say_hello(username=None):
    # 測試用，確定 webhook server 有連通
    return render_template("hello.html",name=username)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 根據不同的使用者事件(Event)，用不同的方式回應
    # eg. MessageEvent 代表使用者傳輸訊息(包含 純文字、圖片、聲音、貼圖...)
    # TextMessageContent 代表使用者傳輸的訊息內容是文字
    # 符合兩者條件的事件會被handler_message 所處理
    response = chat_with_gpt(event.message.text, api_key)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )

if __name__ == "__main__":
    
    app.run(debug=True)  # debug=True 程式碼更動後直接更新到網頁上，不用重新執行 python xxxx.py