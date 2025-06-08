import pytest
from selenium.webdriver.common.by import By


def test_successful_transfer_with_large_balance(browser):
    """TC-01 — Успешный перевод больших сумм"""
    link = "http://localhost:8000/?balance=1000000000000&reserved=100000000"
    card_number = 9999888877776666
    transfer_sum = 10000000000
    expected_alert = f"Перевод {transfer_sum} ₽ на карту {card_number} принят банком!"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()
    transfer_amount_field.send_keys(transfer_sum)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    # Проверяем, что появилось корректное сообщение об успешном переводе
    assert browser.switch_to.alert.text == expected_alert, "Ожидалось сообщение об успешном переводе"


@pytest.mark.xfail(reason="БАГ. Сумма перевода должна быть больше 0")
def test_transfer_with_zero_amount_should_be_blocked(browser):
    """TC-02 — Перевод нулевой суммы (БАГ)"""
    link = "http://localhost:8000/?balance=10000&reserved=0"
    card_number = 1111222233334444
    transfer_sum = 0
    expected_alert = "Cумма должна быть больше нуля"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()
    transfer_amount_field.send_keys(transfer_sum)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    # Проверяем, что появилось сообщение об ошибке для нулевой суммы
    assert browser.switch_to.alert.text == expected_alert, "Ожидалось сообщение об ошибке при нулевой сумме"


def test_transfer_when_balance_equals_reserve_should_be_blocked(browser):
    """TC-03 — Попытка перевода при равенстве баланса и резерва"""
    link = "http://localhost:8000/?balance=10000&reserved=10000"
    card_number = 3333444455556666
    transfer_sum = 1
    expected_message = "Недостаточно средств на счете"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()
    transfer_amount_field.send_keys(transfer_sum)

    error_message = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > span:nth-child(8)")

    # Проверяем, что отображается сообщение о недостатке средств
    assert error_message.text == expected_message, "Ожидалось сообщение 'Недостаточно средств на счете'"


def test_transfer_exceeds_limit_by_one_ruble(browser):
    """TC-04 — Перевод на сумму, превышающую доступный лимит на 1 рубль"""
    link = "http://localhost:8000/?balance=11000&reserved=1000"
    card_number = 1234567812345678
    transfer_sum = 9100
    expected_message = "Недостаточно средств на счете"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()
    transfer_amount_field.send_keys(transfer_sum)

    error_message = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > span:nth-child(8)")

    # Проверяем, что появляется ошибка при превышении доступного лимита
    assert error_message.text == expected_message, "Ожидалось сообщение 'Недостаточно средств на счете'"


@pytest.mark.xfail(reason="БАГ. Перевод с отрицательной суммой не должен быть возможен")
def test_transfer_should_work_on_limit_boundary_but_does_not(browser):
    """TC-05 — Перевод отрицательной суммы (БАГ)"""
    link = "http://localhost:8000/?balance=50000&reserved=0"
    card_number = 1111111111111111
    transfer_sum = -1
    expected_alert = "Некорректная сумма перевода"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()
    transfer_amount_field.send_keys(transfer_sum)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    # Проверяем, что при вводе отрицательной суммы появляется сообщение об ошибке
    assert browser.switch_to.alert.text == expected_alert, "Ожидалось сообщение об ошибке при отрицательной сумме"
