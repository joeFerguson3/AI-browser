from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service("C:/Users/joefe/Documents/random projects/AI-browser/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://amazon.com")

input("hi")
