"""
Базовые тесты для проверки инициализации браузера
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия браузера"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_browser_initialization(driver):
    """
    Тест 1: Проверка инициализации браузера и открытия страницы
    """
    # Открываем главную страницу
    driver.get("http://127.0.0.1:5000")
    
    # Проверяем, что страница открылась (исправлено на правильный заголовок)
    assert "Тестовое приложение" in driver.title or "TestApp" in driver.title
    print(f"Заголовок страницы: {driver.title}")
    
    # Проверяем URL
    assert "127.0.0.1:5000" in driver.current_url
    print(f"URL: {driver.current_url}")


def test_homepage_elements(driver):
    """
    Тест 2: Проверка наличия основных элементов на главной странице
    """
    driver.get("http://127.0.0.1:5000")
    
    # Проверяем заголовок
    welcome_heading = driver.find_element(By.ID, "welcome-heading")
    assert welcome_heading.is_displayed()
    assert "Добро пожаловать" in welcome_heading.text
    print(f"Заголовок найден: {welcome_heading.text}")
    
    # Проверяем кнопку "Начать работу"
    get_started_btn = driver.find_element(By.ID, "get-started-btn")
    assert get_started_btn.is_displayed()
    print("Кнопка 'Начать работу' найдена")
    
    # Проверяем ссылку на логин
    login_link = driver.find_element(By.ID, "login-link")
    assert login_link.is_displayed()
    print("Ссылка 'Войти' найдена")


def test_navigation_to_login(driver):
    """
    Тест 3: Проверка навигации на страницу логина
    """
    driver.get("http://127.0.0.1:5000")
    
    # Кликаем на кнопку "Начать работу"
    get_started_btn = driver.find_element(By.ID, "get-started-btn")
    get_started_btn.click()
    
    # Ждем загрузки страницы логина
    time.sleep(1)
    
    # Проверяем, что перешли на страницу логина
    assert "/login" in driver.current_url
    print(f"Переход на страницу логина: {driver.current_url}")
    
    # Проверяем наличие формы логина
    login_form = driver.find_element(By.ID, "login-form")
    assert login_form.is_displayed()
    print("Форма логина найдена")


def test_page_load_time(driver):
    """
    Тест 4: Проверка времени загрузки страницы
    """
    start_time = time.time()
    driver.get("http://127.0.0.1:5000")
    load_time = time.time() - start_time
    
    # Проверяем, что страница загрузилась быстро (менее 3 секунд)
    assert load_time < 3, f"Страница загружалась слишком долго: {load_time:.2f}s"
    print(f"Время загрузки страницы: {load_time:.2f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
