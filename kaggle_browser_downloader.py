from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def download_kaggle_dataset(dataset_name):

    print("Opening Kaggle...")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    driver.get("https://www.kaggle.com")

    time.sleep(3)

    print("Searching dataset:", dataset_name)

    # find search box
    search = driver.find_element(By.XPATH, "//input[@placeholder='Search']")

    search.send_keys(dataset_name + " dataset")

    search.send_keys(Keys.ENTER)

    time.sleep(5)

    # click first dataset
    first_dataset = driver.find_element(By.XPATH, "(//a[contains(@href,'/datasets/')])[1]")

    first_dataset.click()

    time.sleep(5)

    print("Opening dataset page...")

    # click download button
    try:

        download_button = driver.find_element(By.XPATH, "//button[contains(text(),'Download')]")

        download_button.click()

        print("Dataset download started.")

    except:

        print("Download button not found. You may need to login.")

    time.sleep(10)