import os, sys 

def get_secret_and_token():
    # 從環境變數取得 secret key & access token
    channel_secret = os.getenv('LINEBOT_SECRET_KEY', None)
    channel_access_token = os.getenv('LINEBOT_ACCESS_TOKEN', None)
    openai_api_key = os.getenv('OPENAI_API_KEY', None)
    if channel_secret is None:
        print('Specify LINEBOT_SECRET_KEY as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        print('Specify LINEBOT_ACCESS_TOKEN as environment variable.')
        sys.exit(1)
    if openai_api_key is None:
        print('Specify OPENAI_API_KEY as environment variable.')
        sys.exit(1)
    
    return {
        "LINEBOT_SECRET_KEY": channel_secret,
        "LINEBOT_ACCESS_TOKEN": channel_access_token,
        "OPENAI_API_KEY": openai_api_key
    }