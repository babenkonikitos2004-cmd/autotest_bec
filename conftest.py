"""
conftest.py — общие фикстуры для всех тестов.

Переменные окружения (.env):
    BASE_URL      — базовый URL вакцинации (https://emis-test.miacugra.ru/vaccination)
    DISTRICT_URL  — базовый URL паспорта участка (https://emis-test.miacugra.ru/district)
    TOKEN         — Bearer-токен авторизации (один для всех сервисов)
    PATIENT_ID    — ID пациента по умолчанию
    MO_ID         — ID медицинской организации
"""
import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------------------------------- #
#  env — общий словарь состояния сессии                                      #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
def env():
    """
    Словарь состояния сессии.
    Начальные значения из .env, тесты дописывают созданные ID.
    """
    return {
        "base_url": os.getenv(
            "BASE_URL", "https://emis-test.miacugra.ru/vaccination"
        ),
        "district_url": os.getenv(
            "DISTRICT_URL", "https://emis-test.miacugra.ru/district"
        ),
        "token": os.getenv("TOKEN", ""),
        "patient_id": os.getenv(
            "PATIENT_ID", "00000b30-c43a-423e-9260-d8f3798adddc"
        ),
        "mo_id": os.getenv(
            "MO_ID", "a8fad9fc-161e-4de9-adab-5ac32ae9c460"
        ),
    }


# --------------------------------------------------------------------------- #
#  api_client — единая сессия для всех сервисов                             #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
def api_client(env):
    """
    Сессия requests с предустановленными заголовками авторизации.
    Один клиент для всех сервисов — токен одинаковый.
    """
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": env["token"],
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    yield session
    session.close()