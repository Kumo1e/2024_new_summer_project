import os
from openai import OpenAI
from pprint import pprint
chat_history = dict()

def chat_with_gpt(user_id, user_message, openai_api_key, extra_propt = ""):
    client = OpenAI(api_key=openai_api_key)
    message = user_message + extra_propt
    # 把使用者的訊息加入對話紀錄中
    if user_id in chat_history:
        chat_history[user_id].append(
            {
                "role": "user",
                "content": user_message
            }
        )
    else:
        chat_history[user_id]=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    chat_completion = client.chat.completions.create(
        messages= chat_history[user_id][:-1] + [{"role": "user","content": message,}],
        model="gpt-3.5-turbo",
    )

    response = chat_completion.choices[0].message.content
    # 把ChatGPT的回話加入對話紀錄
    chat_history[user_id].append(
        {
            "role": "system",
            "content": response
        }
    )
    return response

if __name__ == "__main__":
    user_message = "天天睡覺，睡睡平安"
    api_key = os.getenv("OPENAI_API_KEY")
    while True:
        user_message = input("請輸入一句話，開始跟ChatGPT聊天")
        if user_message == "quit":
            print("結束對話")
            break

        if api_key and user_message:
            response = chat_with_gpt(user_message, api_key)
            print(response)

        else:
            print("api key is not found:　", api_key)

        print("History: ")
        pprint(chat_history)
