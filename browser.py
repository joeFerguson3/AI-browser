from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import ollama

service = Service("C:/Users/joefe/Documents/random projects/AI-browser/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://amazon.com")

def get_page():
    return driver.page_source

messages = [
    {"role": "system", "content": "You are an AI in the browser, look at the html code and use selenium commands to follow what the user asks."},
]

while True:
    # Saves user response
    user_input = input(">")
    messages.append({"role": "user", "content": user_input})
    messages.append({"role": "user", "content": "Current HTML: " + get_page()})
    # Generates ai response
    response = ollama.chat(model='gemma3', messages=messages)
    response = response['message']['content']
    messages.append({"role": "assistant", "content": response}) # Saves ai response
    print(response)

    # try:
    #     # Runs command
    #     start = response.index('[')
    #     end = response.index(']')
    #     command = response[start + 1:end]
        
    #     # Allows ai to see page result
    #     messages.append({"role": "user", "content": "this is the result of the command: "})
   
    # except ValueError:
    #     pass