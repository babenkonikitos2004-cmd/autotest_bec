"""
conftest.py — общие фикстуры для всех тестов.

Переключение окружения через переменную ENV в .env:
    ENV=dev   → использует DEV_* URLs
    ENV=test  → использует TEST_* URLs

Запуск на конкретном окружении без правки .env:
    pytest --env=dev
    pytest --env=test
"""
import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


def pytest_addoption(parser):
    """Добавляем флаг --env для переключения окружения из командной строки."""
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Окружение: dev или test (переопределяет ENV из .env)",
    )


def _resolve_env(config) -> str:
    """Возвращает имя окружения: cli-флаг → .env → 'test' по умолчанию."""
    cli = config.getoption("--env", default=None)
    if cli:
        return cli.lower()
    return os.getenv("ENV", "test").lower()


@pytest.fixture(scope="session")
def env(request):
    """
    Словарь состояния сессии.
    URL и токен выбираются по активному окружению (dev/test).
    Тесты дописывают созданные ID прямо в этот словарь.
    """
    active_env = _resolve_env(request.config)

    if active_env == "dev":
        base_url     = os.getenv("DEV_BASE_URL",     "http://vacemisdev.oblteh:8084/vaccination")
        district_url = os.getenv("DEV_DISTRICT_URL", "http://vacemisdev.oblteh:8081/District")
        token        = os.getenv("DEV_TOKEN",         os.getenv("TOKEN", ""))
    else:  # test
        base_url     = os.getenv("TEST_BASE_URL",     "https://emis-test.miacugra.ru/vaccination")
        district_url = os.getenv("TEST_DISTRICT_URL", "https://emis-test.miacugra.ru/district")
        token        = os.getenv("TEST_TOKEN",         os.getenv("TOKEN", ""))

    print(f"\n🔧 Окружение: [{active_env.upper()}]  base_url={base_url}")

    return {
        "active_env":    active_env,
        "base_url":      base_url,
        "district_url":  district_url,
        "token":         token,
        "patient_id":    os.getenv("PATIENT_ID", "00000b30-c43a-423e-9260-d8f3798adddc"),
        "mo_id":         os.getenv("MO_ID",       "a8fad9fc-161e-4de9-adab-5ac32ae9c460"),
    }


@pytest.fixture(scope="session")
def api_client(env):
    """
    Сессия requests с авторизацией.
    Один клиент для всех сервисов — токен одинаковый.
    """
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": env["token"],
            "Content-Type":  "application/json",
            "Accept":        "application/json",
        }
    )
    yield session
    session.close()