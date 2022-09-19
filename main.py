import json
import time
import csv

from dotenv import dotenv_values
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

API_KEY = dotenv_values()["API_KEY"]
CITY = "Jämsä"


def get_coordinates(address, city):
    try:
        api_key = "526085f21db02249269a260310af495a"
        parameters = {
            "access_key": f"{api_key}",
            "query": f"{address}, {city}"
        }
        res = requests.get(f"http://api.positionstack.com/v1/forward",
                        params=parameters
        )

        data = json.dumps(res.json())
        jsondata = json.loads(data)

        lat = jsondata["data"][0]["latitude"]
        lon = jsondata["data"][0]["longitude"]

        return lat, lon
    except Exception as e:
        print(address, e)


driver = webdriver.Chrome()
driver.get(f"https://asunnot.oikotie.fi/myytavat-asunnot?pagination=1&locations=%5B%5B104,6,%22{CITY}%22%5D%5D&cardType=100")
time.sleep(3)
for i in range(0, 12):
    ActionChains(driver) \
        .send_keys(Keys.TAB).perform()

ActionChains(driver)\
    .send_keys(Keys.ENTER).perform()

apartments = []

file = open("houses.csv", "w")
writer = csv.writer(file)

while True:
    cards = driver.find_element(By.CLASS_NAME, "cards").find_elements(By.CLASS_NAME, "cards__card")

    for a in cards:
        parts = a.text.split("\n")
        try:
            # some apartments have different amount of params
            if len(parts) == 6:

                lat, lon = get_coordinates(parts[0], CITY)
                # build integer from price string and append data to list
                apartments.append([int(parts[2][0:-2].replace(" ", "")), lat, lon])
            elif len(parts) == 7:
                lat, lon = get_coordinates(parts[0], CITY)

                apartments.append([int(parts[3][0:-2].replace(" ", "")), lat, lon])
        except Exception as e:
            print(e)
            print(parts)
        time.sleep(0.5)

    next_button = driver.find_element(By.CSS_SELECTOR, "body > main > listing-search > section.content.content--primary-background.center-on-wallpaper.padded.padded--v30-h0.padded--topless.padded--bottomless > div > div > div > pagination > div > div:nth-child(4) > button")
    if next_button.get_property("disabled"):
        break

    next_button.click()
    time.sleep(3)

file = open("houses.csv", "w")
writer = csv.writer(file)
writer.writerow(["price", "lat", "lon"])
writer.writerows(apartments)
