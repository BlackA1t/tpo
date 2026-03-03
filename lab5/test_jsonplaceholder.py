import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

# 1. Тест GET запроса
def test_get_post():
    """Проверяет получение поста №1"""
    url = f"{BASE_URL}/posts/1"
    response = requests.get(url)
    
    # Проверки
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['userId'] == 1
    assert len(data['title']) > 0

# 2. Тест POST запроса
def test_create_post():
    """Проверяет создание нового поста"""
    url = f"{BASE_URL}/posts"
    payload = {
        "title": "Python Test Post",
        "body": "Hello world",
        "userId": 1
    }
    
    # Отправляем POST
    response = requests.post(url, json=payload)
    
    # Ожидаем 201 Created
    assert response.status_code == 201
    
    data = response.json()
    # Проверяем, что вернулись отправленные данные
    assert data['title'] == payload['title']
    assert data['body'] == payload['body']
    assert data['userId'] == payload['userId']
    assert data['id'] == 101 # всегда 101

# 3. Тест PUT запроса
def test_update_post():
    """Проверяет полное обновление поста №1"""
    url = f"{BASE_URL}/posts/1"
    payload = {
        "id": 1,
        "title": "Updated post",
        "body": "Hi",
        "userId": 1
    }
    
    # Отправляем PUT
    response = requests.put(url, json=payload)
    
    # Ожидаем 200 OK
    assert response.status_code == 200
    
    data = response.json()
    assert data['title'] == "Updated post"
