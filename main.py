from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
import os

load_dotenv()

url = ("https://www.linkedin.com/jobs/search/?currentJobId=4175014764&f_AL=true&geoId=101165590&"
       "keywords=Python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
time.sleep(5)

# Click Reject Cookies Button
# time.sleep(2)
# reject_button = driver.find_element(by=By.CSS_SELECTOR, value='button[action-type="DENY"]')
# reject_button.click()

# Sign in
driver.find_element(by=By.XPATH, value="/html/body/div[5]/div/div/section/div/div/div/div[2]/button").click()
driver.find_element(by=By.ID, value="base-sign-in-modal_session_key").send_keys(os.getenv("EMAIL"))
driver.find_element(by=By.ID, value="base-sign-in-modal_session_password").send_keys(os.getenv("PASSWORD"))
driver.find_element(by=By.XPATH, value="/html/body/div[5]/div/div/section/div/div/form/div[2]/button").click()

# You may be presented with a CAPTCHA - Solve the Puzzle Manually
# input("Press Enter when you have solved the Captcha")



# driver.quit()