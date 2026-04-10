import pytest
from selenium import webdriver



@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.implicitly_wait(30)
    browser.maximize_window()
    yield browser
    browser.quit()
