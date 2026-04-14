import pytest
import os
from selenium import webdriver
from dotenv import load_dotenv
from pages.api_class import ApiPage

load_dotenv()


@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def api():
    url = os.getenv("URL")
    return ApiPage(url)
