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
    TextMessage,         # 傳輸回Line官方後台的資料格式
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,       # 傳輸過來的方法
    TextMessageContent,  # 使用者傳過來的資料格式
    ImageMessageContent
)
from get_handle_keys import get_secret_and_token
from openai_api import chat_with_gpt
from cwa_opendata_scraper import get_cyties_weather
import requests

app = Flask(__name__)
keys = get_secret_and_token()
handler = WebhookHandler(keys["LINEBOT_SECRET_KEY"])
configuration = Configuration(access_token=keys["LINEBOT_ACCESS_TOKEN"])
api_key = keys["OPENAI_API_KEY"]
cwa_key = keys["CWA_KEY"]

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
def handle_text_message(event):
    # 根據不同的使用者事件(Event)，用不同的方式回應
    # eg. MessageEvent 代表使用者傳輸訊息(包含 純文字、圖片、聲音、貼圖...)
    # TextMessageContent 代表使用者傳輸的訊息內容是文字
    # 符合兩者條件的事件會被handler_message 所處理
    user_id = event.source.user_id
    user_message = event.message.text
    
    if '天氣如何' in user_message:
        response = handle_weather(user_id, user_message, cwa_key)
    else:
        response = chat_with_gpt(user_id, user_message, api_key)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )

def handle_weather(user_id, user_message, cwa_key):
    locations_name = user_message.split()[1:]
    response = ''
    if locations_name:
        weather_data = get_cyties_weather(cwa_key,locations_name)
        for location in weather_data:
            response += f"{location}:\n"
            for weather in sorted(weather_data[location]):
                response += f"\t\t\t\t{weather}: {weather_data[location][weather]}\n"
        response.strip()
        response = chat_with_gpt(user_id, response, api_key, 
                                extra_propt="請幫我根據上面的內容，生成一段報導，建議使用者的穿搭等等，用100字左右回復")
    else:
        response = "請給我你想知道的縣市，請輸入: 天氣如何 臺中市 臺北市"

    return response

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    image_id = event.message.id
    image_url = f"https://api-data.line.me/v2/bot/message/{image_id}/content"
    header = {'Authorization': f'Bearer {keys["LINEBOT_ACCESS_TOKEN"]}'}
    response = requests.get(image_url, headers=header) # 存圖片
    if response.status_code == 200:
        with open("image_message.jpeg", "wb") as image_file:
            image_file.write(response.content)
        response = "Get image success"
    else:
        response = "Get image failed"
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=response),
                    ImageMessage(originalContentUrl="image_URL",
                                 previewImageUrl="image_URL")
                ]
            )
        )


if __name__ == "__main__":
    
    app.run(debug=True)  # debug=True 程式碼更動後直接更新到網頁上，不用重新執行 python xxxx.py