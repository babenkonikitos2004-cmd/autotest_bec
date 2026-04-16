"""
conftest.py — общие фикстуры для тестов вакцинации.

Использование переменных окружения (.env):
    BASE_URL   — базовый URL API (по умолчанию https://emis-test.miacugra.ru/vaccination)
    TOKEN      — Bearer-токен авторизации
    PATIENT_ID — ID пациента, используемый в тестах редактирования

Пример .env:
    BASE_URL=https://emis-test.miacugra.ru/vaccination
    TOKEN=Bearer eyJhbG...
    PATIENT_ID=00000b30-c43a-423e-9260-d8f3798adddc
"""
from config import VaccinationConfig, DistrictConfig
import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------------------------------- #
#  env — словарь, хранящий состояние сессии (созданные ID и т.п.)            #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
def env():
    """
    Словарь состояния сессии.
    Начальные значения берутся из переменных окружения,
    далее тесты могут дописывать созданные ID.
    """
    return {
        "base_url": os.getenv(
            "BASE_URL", "https://emis-test.miacugra.ru/vaccination"
        ),
        "token": os.getenv("TOKEN", ""),
        "patient_id": os.getenv(
            "PATIENT_ID", "00000b30-c43a-423e-9260-d8f3798adddc"
        ),
    }


# --------------------------------------------------------------------------- #
#  api_client — requests.Session с авторизацией                              #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="session")
def api_client(env):
    """
    Сессия requests с предустановленными заголовками авторизации.
    Переиспользуется во всех тестах сессии.
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