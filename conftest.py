import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


@pytest.fixture(scope='function')
def browser():
    """Фикстура для запуска браузера"""

    options = Options()
    options.add_argument('--headless')  # Без этого на CI не запустится
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)  # ждёт до 5 секунд при поиске каждого элемента
    yield browser
    browser.quit()