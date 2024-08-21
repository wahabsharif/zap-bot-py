import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from io import BytesIO
import pygame

# Directly assign credentials and card details here
USERNAME = "shahzaibalam127@gmail.com"
PASSWORD = "shahzaib000"
CARD_NUMBER = "your_card_number_here"
EXPIRY_DATE = "your_expiry_date_here"
CVV = "your_cvv_here"
OCR_API_KEY = "K81087222088957"  # Replace with your OCR.Space API key

def get_captcha_text(captcha_url):
    try:
        response = requests.get(captcha_url)
        files = {'filename': BytesIO(response.content)}
        data = {'apikey': OCR_API_KEY}
        ocr_response = requests.post('https://api.ocr.space/parse/image', files=files, data=data)
        result = ocr_response.json()
        
        if result['IsErroredOnProcessing']:
            print("Error in OCR processing.")
            return ''
        
        return result['ParsedResults'][0]['ParsedText'].strip()
    except Exception as e:
        print(f"An error occurred during CAPTCHA processing: {e}")
        return ''

def auto_login(driver):
    driver.get("https://blsitalypakistan.com/account/login")
    wait = WebDriverWait(driver, 10)

    try:
        email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter Email']")))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter Password']")
        captcha_image = driver.find_element(By.CSS_SELECTOR, "img[id='Imageid']")
        captcha_field = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter Captcha']")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        email_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)

        captcha_url = captcha_image.get_attribute('src')
        print(f"CAPTCHA URL: {captcha_url}")
        captcha_code = get_captcha_text(captcha_url)
        print(f"Detected CAPTCHA code: {captcha_code}")

        captcha_field.send_keys(captcha_code)
        login_button.click()
    except Exception as e:
        print(f"An error occurred during login: {e}")
        driver.save_screenshot('login_error.png')

def auto_form_fill(driver):
    try:
        form_field_1 = driver.find_element(By.CSS_SELECTOR, "input[name='form_field_1']")
        form_field_2 = driver.find_element(By.CSS_SELECTOR, "input[name='form_field_2']")

        form_field_1.send_keys("Value 1")
        form_field_2.send_keys("Value 2")
    except Exception as e:
        print(f"An error occurred during form filling: {e}")
        driver.save_screenshot('form_fill_error.png')

def auto_relogin(driver):
    if "session expired" in driver.page_source.lower():
        auto_login(driver)

def auto_page_refresh(driver):
    while "no appointments available" in driver.page_source.lower():
        print("No appointments available. Refreshing...")
        time.sleep(5)
        driver.refresh()

def auto_card_details_entry(driver):
    try:
        card_number = driver.find_element(By.CSS_SELECTOR, "input[name='card_number']")
        expiry_date = driver.find_element(By.CSS_SELECTOR, "input[name='expiry_date']")
        cvv = driver.find_element(By.CSS_SELECTOR, "input[name='cvv']")

        card_number.send_keys(CARD_NUMBER)
        expiry_date.send_keys(EXPIRY_DATE)
        cvv.send_keys(CVV)
    except Exception as e:
        print(f"An error occurred during card details entry: {e}")
        driver.save_screenshot('card_details_error.png')

def play_siren():
    pygame.mixer.init()
    pygame.mixer.music.load('siren.mp3')
    pygame.mixer.music.play()

def check_payment_page(driver):
    if "payment" in driver.page_source.lower():
        play_siren()

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        auto_login(driver)
        auto_form_fill(driver)
        auto_page_refresh(driver)
        check_payment_page(driver)
        auto_card_details_entry(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('global_error.png')
    finally:
        driver.quit()
