from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


driver = webdriver.Firefox() 

url = "https://cybersec.ithome.com.tw/2024/speaker"

driver.get(url) 

sp_info_elems = driver.find_elements(By.CLASS_NAME, "sp-info")

speaker_info = []

for sp_info_elem in sp_info_elems:
    name_elem = sp_info_elem.find_element(By.CLASS_NAME, "sp-name")
    name = name_elem.text
    form_elem = sp_info_elem.find_element(By.CLASS_NAME, "sp-form")
    if form_elem:
        form = form_elem.text
    else:
        form = ""
    title_elem = sp_info_elem.find_element(By.CLASS_NAME, "sp-title")
    if title_elem:
        title = title_elem.text
    else:
        title = ""

    speaker_info.append({
        "Name":name,
        "Form":form,
        "Title":title
    })

driver.close()

df = pd.DataFrame(speaker_info)
df.to_csv(r"C:/Users/lenovo/Desktop/speaker_info.csv", index = False)
