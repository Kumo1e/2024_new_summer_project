from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox() # 生成由程式操控的FireFox瀏覽器
driver.get("http://www.python.org") # 訪問
assert "Python" in driver.title  # 檢查 如果錯誤停止程式(報錯)
time.sleep(5)

elem = driver.find_element(By.NAME, "q") 
time.sleep(5)

elem.clear()
elem.send_keys("pycon")
time.sleep(3)

elem.send_keys(Keys.RETURN)
time.sleep(20)

assert "No results found." not in driver.page_source
driver.close() # 關閉分頁
driver.quit() # 關閉整個瀏覽器

print("Done")