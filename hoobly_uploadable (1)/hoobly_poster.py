
import json
import time
import os
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

HOOBLY_USERNAME = os.getenv("HOOBLY_USERNAME")
HOOBLY_PASSWORD = os.getenv("HOOBLY_PASSWORD")

def post_to_hoobly(listing):
    driver = webdriver.Chrome()
    driver.get("https://www.hoobly.com/account/login")

    driver.find_element(By.NAME, "username").send_keys(HOOBLY_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(HOOBLY_PASSWORD)
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    driver.get("https://www.hoobly.com/postad")
    time.sleep(2)

    driver.find_element(By.NAME, "category").send_keys("Dogs and Puppies")
    driver.find_element(By.NAME, "title").send_keys(listing['title'])
    driver.find_element(By.NAME, "price").send_keys(listing['price'])
    driver.find_element(By.NAME, "description").send_keys(listing['description'])
    driver.find_element(By.NAME, "location").send_keys(listing['location'])

    image_upload = driver.find_element(By.NAME, "photo")
    image_upload.send_keys(os.path.abspath("images/" + listing['image_url'].split("/")[-1]))

    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    driver.quit()

def job():
    with open("latest_listing.json", "r") as f:
        listings = json.load(f)
    for listing in listings:
        post_to_hoobly(listing)

schedule.every(20).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
