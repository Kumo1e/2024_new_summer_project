from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.by import By

def create_webdriver():
    return webdriver.Firefox()

def get_exd_card_detail(url, driver):

    driver.get(url) 
    data = dict()

    # 電話
    try:
        tel_elem = driver.find_element(By.CLASS_NAME, "info-tel")
        data["telephone"] = tel_elem.text
    except NoSuchElementException:
        print(f"URL: {url} telephone not found") 

    # 信箱
    try:
        mail_elem = driver.find_element(By.CLASS_NAME, "info-mail")
        data["email"] = mail_elem.text
    except NoSuchElementException:
        print(f"URL: {url} email not found") 


    # Description
    try:
        desc_elem = driver.find_element(By.ID, "ex-foreword")
        data["description"] = desc_elem.text
    except NoSuchElementException:
        print(f"URL: {url} description not found") 


    # Website
    website_elems = driver.find_elements(By.CLASS_NAME, "border-icon")
    for website_elem in website_elems:
        href = website_elem.get_attribute("href")

        if href:
            for social_media_name in ["facebook","linkedin","twitter", "instagram"]:
                if social_media_name in href:
                    data[social_media_name] = href
            else:
                data["website"] = href

    return data

if __name__ == "__main__": # 除非直接呼叫程式檔 否則(import)不執行
    test_driver = create_webdriver() 
    exd_url = "https://cybersec.ithome.com.tw/2024/exhibition-page/1945"
    exd_data = get_exd_card_detail(
        url = exd_url, 
        driver = test_driver
    )
    print(exd_data)
    test_driver.close()
