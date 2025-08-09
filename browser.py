import ollama
from selenium import *
from selenium.webdriver.common.by import *
from selenium.webdriver.support.ui import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress logs

service = Service("C:/Users/joefe/Documents/random projects/AI-browser/chromedriver-win64/chromedriver.exe", log_path="NUL")  # 'NUL' discards logs on Windows
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://amazon.com")
driver.find_element(By.XPATH, "//button[text()='Continue shopping']").click()
time.sleep(10)

def get_page():
    return driver.page_source
def run_code():
    s

messages = [
    {
    "role": "system",
    "content": """You are an assistant that:
1. Reads the provided HTML code.
2. Reads the user's goal.
3. Creates a short plan (1–3 bullet points) on how to get closer to the goal.
4. Outputs exactly ONE line of valid, complete Python Selenium code in this format:
   [driver.find_element(By.<LOCATOR>, "<VALUE>").<ACTION>()]

Strict rules:
- Always close quotes and parentheses correctly.
- The Selenium code must be syntactically correct and executable.
- Always include the action method, e.g., `.click()` if interacting.
- Wrap only the Selenium code in hashtags. No extra spaces or text outside the brackets.

Examples:
HTML: <button id="buy-btn">Buy</button>
Goal: Buy a football.
Plan:
- Locate the buy button by id.
- Click it.
Output: #driver.find_element(By.ID, "buy-btn").click()#

HTML: <button>Continue shopping</button>
Goal: Continue shopping.
Plan:
- Locate the button by text using XPath.
- Click it.
Output: #driver.find_element(By.XPATH, "//button[text()='Continue shopping']").click()#"""
}

]

user_input = input(">")
messages.append({"role": "user", "content": user_input})

goal = False
messages.append({"role": "user", "content": "Current HTML: " + get_page()})
while not goal:
    # Generates ai response
    response = ollama.chat(model='gemma3', messages=messages)
    response = response['message']['content']
    messages.append({"role": "assistant", "content": response}) # Saves ai response
    print(response)

    try:
        # Runs command
        start = response.index('#')
        end = response.index('#')
        command = response[start + 1:end]
        
        # Allows ai to see page result
        try:
            messages.append({"role": "user", "content": "Result from code: " + eval(command)})
        except SyntaxError:
            exec(command)
            time.sleep(5)
            print(get_page())
            messages.append({"role": "user", "content": "Current HTML: " + get_page()})


    except ValueError:
        pass