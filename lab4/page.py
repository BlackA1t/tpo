from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для инициализации драйвера и общих методов."""
    
    def __init__(self, driver):
        self.driver = driver
        self.base_url = Path(__file__).resolve().with_name("index.html").as_uri()

    def open(self):
        """Открывает страницу по URL."""
        self.driver.get(self.base_url)

    def find_element(self, locator, time=10):
        """Ищет элемент с явным ожиданием."""
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Элемент {locator} не найден."
        )

class ContactPage(BasePage):
    """Класс страницы контактов, описывающий локаторы и действия."""

    # Локаторы (инкапсуляция путей к элементам)
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_INPUT = (By.ID, "message")
    SUBMIT_BTN = (By.ID, "submitBtn")
    SUCCESS_MSG = (By.ID, "successMessage")
    ERROR_MSG = (By.ID, "errorMessage")

    def enter_name(self, name):
        self.find_element(self.NAME_INPUT).send_keys(name)

    def enter_email(self, email):
        self.find_element(self.EMAIL_INPUT).send_keys(email)

    def enter_message(self, message):
        self.find_element(self.MESSAGE_INPUT).send_keys(message)

    def click_submit(self):
        self.find_element(self.SUBMIT_BTN).click()

    def get_success_message_text(self):
        """Возвращает текст успешного сообщения, если оно видимо."""
        element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.SUCCESS_MSG)
        )
        return element.text

    def get_error_message_text(self):
        """Возвращает текст ошибки, если он видим."""
        element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MSG)
        )
        return element.text
