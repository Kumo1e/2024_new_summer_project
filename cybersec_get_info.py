import requests
from bs4 import BeautifulSoup
import pandas as pd
from scraper_cybersec import get_exd_card_detail, create_webdriver
import time

def get_cybersec_exd_info(is_export_to_csv=True):
  
    url = "https://cybersec.ithome.com.tw/2024/exhibitionDirectory" 
    response = requests.get(url)


    cybersec_soup = BeautifulSoup(response.text, "html.parser")

    base = "https://cybersec.ithome.com.tw"
    exd_cards = cybersec_soup.find_all("div", attrs ={"class": "exd-card"})

    exd_info = list()

    driver = create_webdriver() 

    for exd_card in exd_cards:
        exd_card_name = exd_card.find("h5").text
        href =  base + exd_card.find("a")["href"]

        if exd_card.h6:
            exd_card_h6 = exd_card.find("h6").text[5:]

        
        # 動態爬蟲抓取廠商資訊
        exd_data = get_exd_card_detail(
            url = href, 
            driver = driver
        )

        # dict1.update(dict2) -> 合併字典的資料
        exd_data.update({
            "name" : exd_card_name,
            "url" : href,
            "id" : exd_card_h6
        })

        exd_info.append(exd_data)

        time.sleep(3)

    driver.close()

    if is_export_to_csv:
        df = pd.DataFrame(exd_info)
        df.to_csv('cybersec.csv',index=False)

    return exd_info

if __name__ == "__main__":
    data = get_cybersec_exd_info()
    print(data[:5])
    print("total: ", len(data))
