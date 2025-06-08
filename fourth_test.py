import pytest
from selenium.webdriver.common.by import By


def test_successful_transfer_valid_data(browser):
    """TC-01 — Успешный перевод с корректными данными"""
    link = "http://localhost:8000/?balance=30000&reserved=20001"
    card_number = "1234567812345678"
    transfer_sum = 5000
    expected_alert = f"Перевод {transfer_sum} ₽ на карту {card_number} принят банком!"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)  # Ввод номера карты

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()  # Очистка поля ввода суммы перевода
    transfer_amount_field.send_keys(transfer_sum)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    assert browser.switch_to.alert.text == expected_alert, "Сообщение во всплывающем окне некорректное"


@pytest.mark.xfail(reason="БАГ. Сумма + комиссия = доступно, но кнопка не активна")
def test_transfer_at_exact_limit_should_pass_but_fails(browser):
    """TC-02 — Перевод на предельную допустимую сумму (БАГ)"""
    link = "http://localhost:8000/?balance=30000&reserved=20001"
    card_number = "1234567812345678"
    transfer_sum = 9099
    expected_alert = f"Перевод {transfer_sum} ₽ на карту {card_number} принят банком!"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)  # Ввод номера карты

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()  # Очистка поля ввода суммы перевода
    transfer_amount_field.send_keys(transfer_sum)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    assert browser.switch_to.alert.text == expected_alert, "Сообщение во всплывающем окне некорректное"


def test_transfer_exceeds_limit_should_be_blocked(browser):
    """TC-03 — Перевод невозможен при превышении лимита"""
    link = "http://localhost:8000/?balance=8000&reserved=3000"
    card_number = "1111222233334444"
    transfer_sum = 6000
    expected_message = "Недостаточно средств на счете"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)  # Ввод номера карты

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()  # Очистка поля ввода суммы перевода
    transfer_amount_field.send_keys(transfer_sum)

    error_message = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > span:nth-child(8)")

    # Проверяем, что появляется сообщение об ошибке: превышение лимита
    assert error_message.text == expected_message, "Текст ошибки не соответствует ожидаемому при превышении лимита"


def test_successful_transfer_with_zero_commission_minimal_amount(browser):
    """TC-04 — Успешный перевод минимальной суммы с нулевой комиссией"""
    link = "http://localhost:8000/?balance=30000&reserved=20001"
    card_number = "1111222233334444"
    transfer_sum = 9
    expected_alert = f"Перевод {transfer_sum} ₽ на карту {card_number} принят банком!"
    expected_comission = 0

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)  # Ввод номера карты

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()  # Очистка поля ввода суммы перевода
    transfer_amount_field.send_keys(transfer_sum)

    comission = int(browser.find_element(By.CSS_SELECTOR, "#comission").text)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    assert comission == expected_comission, f"Комиссия {comission}, ожидалась {expected_comission}"
    assert browser.switch_to.alert.text == expected_alert, "Сообщение во всплывающем окне некорректное"

@pytest.mark.xfail(reason="БАГ. Перевод с отрицательной суммой не должен быть возможен")
def test_negative_transfer_amount_should_be_blocked(browser):
    """TC-05 — Ввод отрицательной суммы перевода (БАГ)"""
    link = "http://localhost:8000/?balance=30000&reserved=20001"
    card_number = "1234567812345678"
    transfer_sum = -5000
    expected_alert = "Сумма должна быть положительной"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)  # Ввод номера карты

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()  # Очистка поля ввода суммы перевода
    transfer_amount_field.send_keys(transfer_sum)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    assert browser.switch_to.alert.text == expected_alert, "Сообщение во всплывающем окне некорректное"
