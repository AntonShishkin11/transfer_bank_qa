import pytest
from selenium import webdriver


@pytest.fixture(scope='function')
def browser():
    """Фикстура для запуска браузера"""
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)  # ждёт до 5 секунд при поиске каждого элемента
    yield browser
    browser.quit()