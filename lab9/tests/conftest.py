import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL

@pytest.fixture()
def session() -> requests.Session:
    s = requests.Session()
    yield s
    s.close()
