"""
Автотесты для проверки функциональности логина
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия браузера"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_login_page_elements(driver):
    """
    Тест 5: Проверка наличия всех элементов на странице логина
    """
    driver.get(f"{BASE_URL}/login")
    
    # Проверяем заголовок страницы
    login_title = driver.find_element(By.ID, "login-title")
    assert login_title.is_displayed()
    assert "Вход в систему" in login_title.text
    print(f"Заголовок: {login_title.text}")
    
    # Проверяем поле username
    username_field = driver.find_element(By.ID, "username")
    assert username_field.is_displayed()
    assert username_field.get_attribute("type") == "text"
    print("Поле 'username' найдено")
    
    # Проверяем поле password
    password_field = driver.find_element(By.ID, "password")
    assert password_field.is_displayed()
    assert password_field.get_attribute("type") == "password"
    print("Поле 'password' найдено")
    
    # Проверяем кнопку входа
    login_button = driver.find_element(By.ID, "login-button")
    assert login_button.is_displayed()
    assert "Войти" in login_button.text
    print("Кнопка 'Войти' найдена")
    
    # Проверяем блок с тестовыми credentials
    test_credentials = driver.find_element(By.ID, "test-credentials")
    assert test_credentials.is_displayed()
    print("Блок с тестовыми данными найден")


def test_successful_login_admin(driver):
    """
    Тест 6: Успешный логин с валидными credentials (admin)
    """
    driver.get(f"{BASE_URL}/login")
    
    # Находим элементы формы
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    
    # Вводим данные
    username_field.clear()
    username_field.send_keys("admin")
    password_field.clear()
    password_field.send_keys("admin123")
    
    print("Данные введены: admin / admin123")
    
    # Кликаем кнопку входа
    login_button.click()
    
    # Ждем перенаправления на dashboard
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )
    
    # Проверяем, что перешли на dashboard
    assert "/dashboard" in driver.current_url
    print(f"Перенаправление на: {driver.current_url}")
    
    # Проверяем наличие приветствия с именем пользователя
    user_greeting = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-greeting"))
    )
    assert "admin" in user_greeting.text.lower()
    print(f"Приветствие: {user_greeting.text}")
    
    # Проверяем наличие кнопки Logout
    logout_link = driver.find_element(By.ID, "logout-link")
    assert logout_link.is_displayed()
    print("Кнопка 'Выйти' отображается")
    
    # Проверяем заголовок dashboard
    dashboard_title = driver.find_element(By.ID, "dashboard-title")
    assert "Панель управления" in dashboard_title.text
    print(f"Заголовок dashboard: {dashboard_title.text}")


def test_successful_login_testuser(driver):
    """
    Тест 7: Успешный логин с другим пользователем (testuser)
    """
    driver.get(f"{BASE_URL}/login")
    
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    
    username_field.send_keys("testuser")
    password_field.send_keys("Test@2024")
    login_button.click()
    
    # Проверяем успешный вход
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "logout-link"))
    )
    
    current_user = driver.find_element(By.ID, "current-user")
    assert "testuser" in current_user.text
    print(f"Успешный вход для пользователя: {current_user.text}")


def test_invalid_login_wrong_password(driver):
    """
    Тест 8: Неуспешный логин с неверным паролем
    """
    driver.get(f"{BASE_URL}/login")
    
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    
    # Вводим правильный username, но неверный пароль
    username_field.send_keys("admin")
    password_field.send_keys("wrongpassword")
    login_button.click()
    
    # Ждем сообщения об ошибке
    flash_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash-message"))
    )
    
    # Проверяем сообщение об ошибке
    assert flash_message.is_displayed()
    assert "Неверное имя пользователя или пароль" in flash_message.text
    print(f"Сообщение об ошибке: {flash_message.text}")
    
    # Проверяем, что остались на странице логина
    assert "/login" in driver.current_url
    print("Остались на странице логина")


def test_invalid_login_wrong_username(driver):
    """
    Тест 9: Неуспешный логин с несуществующим пользователем
    """
    driver.get(f"{BASE_URL}/login")
    
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    
    username_field.send_keys("nonexistentuser")
    password_field.send_keys("somepassword")
    login_button.click()
    
    # Проверяем сообщение об ошибке
    flash_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash-message"))
    )
    
    assert "Неверное имя пользователя или пароль" in flash_message.text
    print(f"Ошибка при несуществующем пользователе: {flash_message.text}")


def test_empty_fields_validation(driver):
    """
    Тест 10: Проверка валидации пустых полей
    """
    driver.get(f"{BASE_URL}/login")
    
    login_button = driver.find_element(By.ID, "login-button")
    
    # Нажимаем кнопку входа с пустыми полями
    login_button.click()
    
    # Ждем сообщения об ошибке
    flash_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash-message"))
    )
    
    assert "Заполните все поля" in flash_message.text
    print(f"Валидация пустых полей работает: {flash_message.text}")


def test_logout_functionality(driver):
    """
    Тест 11: Проверка функциональности выхода из системы
    """
    # Сначала логинимся
    driver.get(f"{BASE_URL}/login")
    
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    
    username_field.send_keys("demo")
    password_field.send_keys("demo_password")
    login_button.click()
    
    # Ждем загрузки dashboard
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "logout-link"))
    )
    
    print("Успешно вошли в систему")
    
    # Кликаем на кнопку выхода
    logout_link = driver.find_element(By.ID, "logout-link")
    logout_link.click()
    
    # Проверяем, что вернулись на главную страницу
    WebDriverWait(driver, 10).until(
        EC.url_to_be(BASE_URL + "/")
    )
    
    assert driver.current_url == BASE_URL + "/"
    print(f"Перенаправление после logout: {driver.current_url}")
    
    # Проверяем, что больше нет кнопки logout
    logout_links = driver.find_elements(By.ID, "logout-link")
    assert len(logout_links) == 0
    print("Кнопка 'Выйти' больше не отображается")


def test_protected_page_access_without_login(driver):
    """
    Тест 12: Проверка доступа к защищенной странице без авторизации
    """
    # Пытаемся напрямую открыть dashboard без логина
    driver.get(f"{BASE_URL}/dashboard")
    
    # Должны быть перенаправлены на страницу логина
    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )
    
    assert "/login" in driver.current_url
    print("Без авторизации перенаправлено на /login")
    
    # Проверяем сообщение о необходимости входа
    flash_message = driver.find_element(By.ID, "flash-message")
    assert "Пожалуйста, войдите в систему" in flash_message.text
    print(f"Сообщение: {flash_message.text}")


def test_form_field_attributes(driver):
    """
    Тест 13: Проверка атрибутов полей формы для автозаполнения
    """
    driver.get(f"{BASE_URL}/login")
    
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    # Проверяем autocomplete атрибуты
    assert username_field.get_attribute("autocomplete") == "username"
    print("Атрибут autocomplete для username: username")
    
    assert password_field.get_attribute("autocomplete") == "current-password"
    print("Атрибут autocomplete для password: current-password")
    
    # Проверяем placeholder
    assert username_field.get_attribute("placeholder") is not None
    assert password_field.get_attribute("placeholder") is not None
    print("Placeholder атрибуты присутствуют")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
