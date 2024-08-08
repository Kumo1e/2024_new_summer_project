Line Bot 初始設定(第一次使用需要執行1.~3.) # 櫃台
1. Line Messaging API -> Start Now 登入Line 帳號
2. 新建Chennal 來當作 Line Bot 使用
3. 開啟Webohook  Messaging API -> Auto-reply messages -> Edit 
重要資訊取得位置(*注意*不要控管)
   * Chennal Secret & user ID 在 Basic setting
   * Access Token 在 Messaging API
   1. 使用環境變數設定(儲存在本地的電腦裡，更換電腦需要重建)
       * 開啟環境變數 -> 環境變數 -> 使用者環境變數 -> 新增 輸入"變數名稱" + your secret ket
       * 開啟環境變數 -> 環境變數 -> 使用者環境變數 -> 新增 輸入"變數名稱" + your access token
        程式檔案內使用 import os -> object = os.getenv("變數名稱")
        (如果報錯重新開啟VSC)
------------------------------------------------------------------------------------------
4. Webhook 網址(會更動)填寫 -> Messaging API 
   -> Webhook URL 填入 Ngrok取得的網址，要加上\route_name
   -> Edit -> Verify 回傳Success就成功啦 (下面的 Use Webhook 要打開)


LINE Offical Account Manager 官方帳號Chennal控管
1. Line Chat 聊天: 可以看到 Chennal 內成員的訊息

Ngrok 設定 (第一次使用需要執行1.~3.) # 總機
1. 登入 Ngrok :https://ngrok.com/
2. 下載檔案 .zip -> 解壓縮 -> ngrok.exe 檔案放到開發資料夾中
3. 在下載網頁複製程式碼 ngrok config add-authtoken AUTH_TOKEN -> powershell中執行 分機(本地端)與總機連線
------------------------------------------------------------------------------------------
4. 執行 .\ngrok http 5000 (5000是因為 flask 預設跑在5000 port) 持續開著
   -> 取得網址 https://xxxx.ngrok-free.app (每次開啟都會不一樣) 
   

下載相關模組
* pip install flask  # 簡易網頁設計模組
* pip install line-bot-sdk # Linebot 模組
參考文件: https://github.com/line/line-bot-sdk-python
