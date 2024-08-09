import os
from openai import OpenAI

def chat_with_gpt(user_message:any, openai_api_key:any) -> str:
    client = OpenAI(api_key=openai_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_message + "請用有感情的方式回答一句話就好",
            }
        ],
        model="gpt-3.5-turbo",
    )

    response = chat_completion.choices[0].message.content
    return response

if __name__ == "__main__":
    user_message = "天天睡覺，睡睡平安"
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and user_message:
        response = chat_with_gpt(user_message, api_key)
        print(response)

