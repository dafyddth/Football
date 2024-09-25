from typing import Optional
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


def get_page_source(my_url):
    options = Options()
    options.add_argument("--window-size=1920,1080")  # set window size to native GUI size

    # Disable images
    options.set_preference("permissions.default.image", 2)

    driver = webdriver.Firefox(options=options)
    driver.set_window_position(-10000, 0)  # move the window off-screen

    driver.get(my_url)
    time.sleep(2)
    html = driver.page_source
    driver.close()
    return html
