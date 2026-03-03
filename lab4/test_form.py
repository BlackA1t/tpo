import pytest
from selenium import webdriver
from page import ContactPage

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_positive_submission(browser):
    """
    Позитивный сценарий:
    1. Открыть страницу.
    2. Заполнить валидными данными (Имя, Email).
    3. Отправить форму.
    4. Проверить текст успешного сообщения.
    """
    page = ContactPage(browser)
    page.open()
    
    page.enter_name("Иван Иванов")
    page.enter_email("ivan@example.com")
    page.enter_message("Тестовое сообщение")
    page.click_submit()
    
    assert "Сообщение успешно отправлено!" in page.get_success_message_text()

def test_negative_empty_email(browser):
    """
    Негативный сценарий:
    1. Открыть страницу.
    2. Заполнить Имя, но оставить Email пустым.
    3. Отправить форму.
    4. Проверить появление ошибки валидации.
    """
    page = ContactPage(browser)
    page.open()
    
    page.enter_name("Иван Безпочты")
    # Email не заполняем
    page.click_submit()
    
    assert "Ошибка: Поле Email обязательно" in page.get_error_message_text()
