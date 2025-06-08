import pytest
from selenium.webdriver.common.by import By


@pytest.mark.xfail(reason="БАГ. перевод должен проходить")
def test_minimal_amount_transfer_should_succeed_but_fails(browser):
    """TC-01 — Успешный перевод минимальных сумм (БАГ)"""
    link = "http://localhost:8000/?balance=1&reserved=0"
    card_number = 1234567812345678
    transfer_sum = 1
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


@pytest.mark.xfail(reason="БАГ. Должна появляться ошибка 'Некорректный номер карты'")
def test_invalid_card_number_all_zeros_should_be_blocked(browser):
    """TC-02 — Невалидный номер карты (БАГ)"""
    link = "http://localhost:8000/?balance=30000&reserved=10000"
    card_number = "0000000000000000"
    transfer_sum = 1000
    expected_alert = "Некорректный номер карты"

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


def test_transfer_at_limit_boundary_should_succeed(browser):
    """TC-03 — Перевод при корректной комиссии и границе"""
    link = "http://localhost:8000/?balance=10000&reserved=1000"
    card_number = 4321567834524673
    transfer_sum = 8182
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


@pytest.mark.xfail(reason="БАГ. Комиссия должна составлять 99 руб.")
def test_commission_calculation_should_round_down_fraction(browser):
    """TC-04 — Проверка корректности расчёта комиссии при дробном результате (БАГ)"""
    link = "http://localhost:8000/?balance=10000&reserved=0"
    card_number = 1234567812345678
    transfer_sum = 999
    expected_comission = 99
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

    comission = int(browser.find_element(By.CSS_SELECTOR, "#comission").text)

    transfer_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > button")
    transfer_button.click()

    assert comission == expected_comission, "Комиссия должна составлять 10% от суммы перевода"
    assert browser.switch_to.alert.text == expected_alert, "Сообщение во всплывающем окне некорректное"


def test_sum_input_field_visible_only_after_16_digit_card_input(browser):
    """TC-5 — Поле суммы отображается только после ввода 16 цифр карты"""
    link = "http://localhost:8000/?balance=10000&reserved=0"
    card_number_15 = 123456781234567
    card_num_1 = 8

    browser.get(link)
    account_button = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div > div:nth-child(1)")
    account_button.click()

    card_number_field = browser.find_element(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]")
    card_number_field.send_keys(card_number_15)

    # Проверяем, что поле суммы отсутствует
    sum_fields = browser.find_elements(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    assert len(sum_fields) == 0, "Поле суммы не должно отображаться при 15-значном номере карты"

    # Вводим 16-ю цифру
    card_number_field.send_keys(card_num_1)

    # Проверяем, что поле суммы появилось
    sum_fields = browser.find_elements(By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > input[type=text]:nth-child(5)")
    assert len(sum_fields) == 1, "Поле суммы должно отображаться при 16-значном номере карты"
