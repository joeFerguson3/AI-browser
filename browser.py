import ollama
from selenium import *
from selenium.webdriver.common.by import *
from selenium.webdriver.support.ui import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress logs

service = Service("C:/Users/joefe/Documents/random projects/AI-browser/chromedriver-win64/chromedriver.exe", log_path="NUL")  # 'NUL' discards logs on Windows
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.amazon.com/exec/obidos/subst/home/home.html")

def get_page():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return str(soup.body)

def run_code():
    try:
        # Allows ai to see page result
        exec(command)
        time.sleep(5)
        messages.append({"role": "user", "content": "The HTML for the current page is: " + get_page()
                        + "Current URL: " + driver.current_url + "continue completing the users goal, do not give an explanation or an analyse of the html"})
    except (NoSuchElementException, TypeError, AttributeError) as e:
        messages.append({"role": "user", "content": "There was an exception: " + str(e)})

messages = [
    {
    "role": "system",
    "content": "AI Browser Navigation Instructions: 1. Always enclose exactly one Selenium command per response in hashtags: #command#. 2. To open a webpage, use: #driver.get('URL')#. 3. To locate an element, use: #element = driver.find_element(By.METHOD, 'selector')#. 4. To interact with an element: click: #element.click()#, type text: #element.send_keys('text')#. 5. To navigate browser history or refresh: back: #driver.back()#, forward: #driver.forward()#, refresh: #driver.refresh()#. 6. To find multiple elements: #elements = driver.find_elements(By.METHOD, 'selector')#. 7. Use explicit waits or time.sleep(seconds) if needed to allow page loading before next step. 8. Confirm each step is complete or element exists before proceeding. 9. Respond only with the next Selenium command enclosed in #, no extra text or explanation. 10. Do not repeatedly run the same line of selenium.do not give an explanation or an analyse of the html"
}

]

messages.append({"role": "user", "content": "The HTML for the current page is: " + get_page()
                        + "Current URL: " + driver.current_url})

user_input = input(">")
messages.append({"role": "user", "content": "User goal: " + user_input})

goal = False

while not goal:
    # Generates ai response
    response = ollama.chat(model='gemma3', messages=messages)
    response = response['message']['content']
    messages.append({"role": "assistant", "content": response}) # Saves ai response
    print(response)

    try:
        # Runs command
        start = response.find('#')  
        end = response.find('#', start + 1)
        command = response[start + 1:end]
        print(command)
        run_code()

    except ValueError:
        pass