import requests
from logging import *
import time 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

# Set Firefox options for headless mode
options = Options()
options.headless = True

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)
basicConfig(level=INFO)

url = "https://ieltstehran.com/computer-delivered-ielts-exam/"


def send_notification():
    try:
        # Construct the URL for sending a message to Telegram using the provided bot_token
        telegram_url = f'https://api.telegram.org/bot6425159161:AAGAlkU22DrzfcoYJbXxtfQVTyCkmF2shVE/sendMessage'

        # Prepare the data to be sent in the POST request
        data = {
            'chat_id': -1001790575888,
            'text': f"""
            Digital Exam available on IELTS Tehran!

{url}
            """,
        }

        # Send the POST request to the Telegram API
        response = requests.post(telegram_url, data=data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            info('Message sent to telegram successfully')
            return True
        else:
            # If the request was not successful, print an error message and the response text
            error(
                f'Failed to send message. Status code: {response.status_code}')
            error(response.text)

            return False
    except Exception as e:
        # Handle any exceptions that may occur during the execution of the code
        error(f'Error: {e}')
        return False


def refresh():
    info("opening schedule page\n")
    driver.get(url)


def check_table():
    time.sleep(5)
    try:
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "myTable")))

        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        if "درحال بارگذاری" in tbody.text:
            check_table()
            return

        if "موردی جهت نمایش وجود ندارد" == tbody.text:
            raise Exception("Table is empty. trying again...")

        send_notification()
    except StaleElementReferenceException:
        info("No table found!")
        check_table()


def main():
    try:
        refresh()
        check_table()
    except Exception as e:
        error(e)
        main()


if __name__ == '__main__':
    main()
