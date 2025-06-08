import pytest
from selenium.webdriver.common.by import By


def test_successful_transfer_with_zero_commission(browser):
    """TC-01 — Успешный перевод на сумму с нулевой комиссией"""
    link = "http://localhost:8000/?balance=1000&reserved=0"
    card_number = 1111222233334444
    transfer_sum = 1
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

    # Проверяем, что сообщение от банка совпадает с ожидаемым
    assert browser.switch_to.alert.text == expected_alert, "Текст уведомления не соответствует ожидаемому"


@pytest.mark.xfail(reason="БАГ. Комиссия должна быть 10% от суммы перевода")
def test_comission_rounding(browser):
    """TC-02 — Перевод суммы с округлением комиссии вниз (БАГ)"""
    link = "http://localhost:8000/?balance=1000&reserved=0"
    card_number = 1234567812345678
    transfer_sum = 99
    expected_comission = int(transfer_sum * 10 / 100)
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

    comission = int(browser.find_element(By.CSS_SELECTOR, "#comission").text)

    # Проверяем, что рассчитанная комиссия равна ожидаемой (должна быть 9)
    assert comission == expected_comission, f"Комиссия {comission}, ожидалась {expected_comission}"

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    # Проверяем, что уведомление от банка совпадает с ожидаемым
    assert browser.switch_to.alert.text == expected_alert, "Текст уведомления не соответствует ожидаемому"


@pytest.mark.xfail(reason="БАГ. Перевод не должен проходить, должна появляться ошибка")
def test_card_number_17_digits(browser):
    """TC-03 — Ввод невалидного номера карты (БАГ)"""
    link = "http://localhost:8000/?balance=15000&reserved=0"
    card_number = 12345678123456789  # 17 цифр
    transfer_sum = 1000
    expected_alert = "Введите корректный номер карты (16 цифр)"

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

    # Проверяем, что появляется сообщение об ошибке валидации (должна быть ошибка, но её нет)
    assert browser.switch_to.alert.text == expected_alert, "Ожидалось сообщение об ошибке валидации номера карты"


def test_transfer_exceeds_limit_after_commission_should_be_blocked(browser):
    """TC-04 — Превышение доступной суммы после учёта комиссии"""
    link = "http://localhost:8000/?balance=10000&reserved=2000"
    card_number = 2222333344445555
    transfer_sum = 8000
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

    # Проверяем, что появляется сообщение об ошибке: превышение лимита
    assert error_message.text == expected_message, "Текст ошибки не соответствует ожидаемому при превышении лимита"


@pytest.mark.xfail(reason="БАГ. Перевод не должен проходить, должна появляться ошибка")
def test_transfer_without_amount_should_be_blocked(browser):
    """TC-05 — Перевод без ввода суммы (БАГ)"""
    link = "http://localhost:8000/?balance=20000&reserved=0"
    card_number = 1111222233334444
    expected_alert = "Недостаточно средств на счете"

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number)

    transfer_amount_field = browser.find_element(By.CSS_SELECTOR,
                                                 "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    transfer_amount_field.clear()  # Поле суммы остаётся пустым

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    # Проверяем, что появляется сообщение об ошибке при пустом поле суммы
    assert browser.switch_to.alert.text == expected_alert, "Ожидалось сообщение об ошибке при пустом поле суммы"


