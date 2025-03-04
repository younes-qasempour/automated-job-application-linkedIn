from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

load_dotenv()

def abort_application(driver):
    try:
        close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_button.click()
    except NoSuchElementException:
        print("Close button not found in abort application.")

    time.sleep(4)
    try:
        discard_button = driver.find_element(By.CSS_SELECTOR, '[data-control-name="discard_application_confirm_btn"]')
        time.sleep(2)
        discard_button.click()
    except (NoSuchElementException, IndexError):
        print("Discard button not found in abort application.")

url = ("https://www.linkedin.com/jobs/search/?currentJobId=4154785477&distance=25&f_AL=true&geoId=101165590&keywords"
       "=Python%20developer&origin=JOB_SEARCH_PAGE_KEYWORD_HISTORY&refresh=true")

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
input("Press Enter when you have solved the Captcha")

# Get Listings
time.sleep(5)
all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable div")

for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(2)
    try:
        # Click Apply Button
        apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-apply-button")
        apply_button.click()

        # Insert Phone Number
        time.sleep(5)
        phone_number = os.getenv("PHONE_NUMBER")
        if phone_number is None:
            print("PHONE_NUMBER environment variable is not set. Please update your .env file.")
            driver.quit()
            exit(1)
        phone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id*=phoneNumber]")))
        if phone.get_attribute("value") == "":
            phone.send_keys(phone_number)

        # Check the Submit Button
        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            abort_application(driver)
            print("Complex application, skipped.")
            continue
        else:
            # Click Submit Button
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        # Click Close Button
        try:
            close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
            close_button.click()
        except NoSuchElementException:
            print("Close button not found, assuming modal has closed.")

    except NoSuchElementException:
        abort_application(driver)
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()