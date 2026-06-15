# Autotest BEC — автотесты вакцинации (API)

Регламент для команды тестирования: как взять проект, настроить, запускать тесты и вносить изменения, не ломая друг другу работу.

Если коротко: **не пишем в `main` напрямую**. Каждый работает в своей ветке, прогоняет тесты локально, отправляет Pull Request, после ревью — мерж в `main`.

---

## 1. Что это за проект

Набор API-автотестов на `pytest + requests` для сервиса вакцинации. Тесты проверяют CRUD по основным сущностям:

| Файл | Что покрывает |
|------|---------------|
| `tests/test_vaccine.py` | Выполненные прививки (`/Vaccine`) |
| `tests/test_vaccine_plan.py` | Запланированные прививки (`/Vaccine/plan`) |
| `tests/test_probe.py` | Выполненные пробы (`/Probe`) |
| `tests/test_probe_plan.py` | Запланированные пробы (`/ProbePlan`) |
| `tests/test_exemption.py` | Медотводы / отказы (`/Exemption`) |
| `tests/test_district.py` | Участки (district-сервис) |
| `tests/test_reference_info.py` | Справочная информация: News / Review / File (`vac-report`) |

Тесты умеют работать на двух контурах — **dev** и **test** — переключение через `.env` или флаг командной строки.

---

## 2. Требования

- Python **3.11+** (проект гоняется и на 3.14)
- `git`
- Доступ к нужному контуру:
  - **test** (`https://emis-test.miacugra.ru`) — доступен извне;
  - **dev** (`vacemisdev.oblteh`) — **только из внутренней сети**. Если ты не в ней, dev-тесты упадут по таймауту/connection, и это не баг кода.

---

## 3. Установка (один раз)

```bash
# 1. Клонируем
git clone https://github.com/babenkonikitos2004-cmd/autotest_bec.git
cd autotest_bec

# 2. Виртуальное окружение
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Зависимости
pip install -r requirements.txt

# 4. Конфиг окружения (см. раздел 4)
copy .env.example .env      # Windows
# cp .env.example .env      # Linux / macOS
```

---

## 4. Настройка окружения (`.env`)

Файл `.env` **не хранится в git** (см. раздел 9) — у каждого свой локальный. Создаётся копированием из `.env.example` и заполняется актуальными токенами.

```dotenv
# Какой контур использовать по умолчанию: dev или test
ENV=test

# --- Dev (внутренняя сеть) — пути от корня сервиса, БЕЗ префиксов ---
DEV_BASE_URL=http://vacemisdev.oblteh:8084
DEV_DISTRICT_URL=http://vacemisdev.oblteh:8081
DEV_VAC_REPORT_URL=            # адрес vac-report на dev; пусто → эти тесты скипаются
DEV_TOKEN=Bearer <jwt>

# --- Test (за шлюзом) — пути С префиксами /vaccination, /district, /vac-report ---
TEST_BASE_URL=https://emis-test.miacugra.ru/vaccination
TEST_DISTRICT_URL=https://emis-test.miacugra.ru/district
TEST_VAC_REPORT_URL=https://emis-test.miacugra.ru/vac-report
TEST_TOKEN=Bearer <jwt>

# --- Общие ---
PATIENT_ID=00000b30-c43a-423e-9260-d8f3798adddc
MO_ID=a8fad9fc-161e-4de9-adab-5ac32ae9c460
```

### Важно про различие контуров

- **dev** — сервисы раскиданы по портам, и каждый отдаёт пути **от корня** (`/Probe/NEW`). Префикс `/vaccination` тут **не нужен**.
- **test** — всё за общим шлюзом, поэтому пути идут **с префиксом** (`/vaccination/Probe/NEW`, `/vac-report/Review` и т.д.).

Если перепутать префиксы — сервер ответит `500 No endpoint ...`.

### Токены

`*_TOKEN` — это JWT с полем `exp` (срок жизни). Когда токен протух, тесты начнут возвращать `401`. Тогда нужно получить свежий токен и заменить значение в своём `.env`. Токен в репозиторий не коммитим.

---

## 5. Запуск тестов

```bash
# Все тесты на контуре из .env
pytest

# Конкретный контур (флаг перебивает .env)
pytest --env=test
pytest --env=dev

# Один файл
pytest tests/test_vaccine_plan.py

# Один класс / один тест
pytest tests/test_probe.py::TestProbe
pytest tests/test_probe.py::TestProbe::test_create_executed_probe

# По подстроке в имени
pytest -k "create"

# Подробный вывод
pytest -v
```

В начале прогона `conftest.py` печатает, на какой контур пошли — **всегда проверяй первую строку**:

```
🔧 Окружение: [TEST]  base_url=https://emis-test.miacugra.ru/vaccination
```

> Тесты `vac-report` (News / Review / File) на **dev** будут `SKIPPED`, пока в `.env` не заполнен `DEV_VAC_REPORT_URL`. Это ожидаемо.

В проекте также есть `run_tests.py` — обёртка для запуска (например, с генерацией отчёта). Запуск: `python run_tests.py`.

---

## 6. Git-workflow (главное правило)

`main` — **стабильная** ветка. В неё попадает только проверенный код через Pull Request. Напрямую в `main` не пушим.

### Жизненный цикл задачи

```bash
# 1. Перед началом — забираем свежий main
git checkout main
git pull origin main

# 2. Создаём ветку под задачу
git checkout -b feature/vaccine-edit-validation

# 3. Работаем, прогоняем тесты локально
pytest -v

# 4. Коммитим (осмысленно, маленькими порциями)
git add tests/test_vaccine.py
git commit -m "fix: убрал обращение к env через точку в test_edit_vaccine"

# 5. Пушим ветку
git push -u origin feature/vaccine-edit-validation

# 6. На GitHub открываем Pull Request: feature/... -> main
#    Описываем что сделали, прикладываем результат прогона.

# 7. После аппрува мерж в main, ветку удаляем.
```

### Именование веток

| Префикс | Когда | Пример |
|---------|-------|--------|
| `feature/` | новые тесты / сущности | `feature/add-district-tests` |
| `fix/` | починка падающих тестов | `fix/probe-plan-id-ref` |
| `chore/` | инфраструктура, конфиги, зависимости | `chore/update-gitignore` |

Можно также именовать по тестеру: `nikita/exemption-cleanup`. Главное — единообразно в команде.

### Сообщения коммитов

Короткое, в настоящем времени, по сути:

```
fix: вернул /vaccination только на test-контур
feature: тесты CRUD для участков (district)
chore: .env добавлен в .gitignore
```

### Перед Pull Request

1. `git pull origin main` в свою ветку (подтянуть чужие изменения, разрулить конфликты).
2. `pytest` — прогон зелёный (или объяснено, почему что-то падает/скипается).
3. В описании PR: что меняли, на каком контуре гоняли, скрин/лог результата.

### Что НЕ коммитим

- свой `.env` с токенами;
- `__pycache__/`, `.pytest_cache/`, `.venv/`;
- результаты прогонов (`allure-results/`, отчёты) — если не договорились иначе.

---

## 7. Правила написания тестов

Чтобы тесты не ломались при переключении контуров и не зависели друг от друга:

**URL берём только из `env`, не хардкодим.**
```python
# плохо
resp = api_client.put("https://emis-test.miacugra.ru/vac-report/Review", ...)
# хорошо
resp = api_client.put(f"{env['vac_report_url']}/Review", ...)
```

**`env` — это обычный словарь.** Доступ только по ключу, не через точку:
```python
plan_id = env.get("created_vaccine_plan_id")   # ок
plan_id = env["created_vaccine_plan_id"]       # ок
plan_id = env.created_vaccine_plan_id          # AttributeError!
```

**ID созданных объектов прокидываем через `env`**, а не хардкодим:
```python
def test_create_...(self, api_client, env):
    ...
    env["created_vaccine_id"] = data["id"]      # сохранили

def test_edit_...(self, api_client, env):
    vaccine_id = env.get("created_vaccine_id")  # переиспользовали
    if not vaccine_id:
        pytest.skip("created_vaccine_id не задан — пропущен тест создания")
```

**Порядок внутри сущности важен:** create → edit → delete. Если create не отработал — edit/delete должны `skip`, а не падать.

**После себя убираем:** созданные в тестах объекты удаляем в `delete`-тестах, чтобы не засорять стенд.

**Доступные ключи `env`:** `active_env`, `base_url`, `district_url`, `vac_report_url`, `token`, `patient_id`, `mo_id` (+ те `created_*_id`, что дописывают сами тесты).

---

## 8. Частые ошибки и что они значат

| Симптом | Причина | Что делать |
|---------|---------|-----------|
| `MissingSchema: No scheme supplied '/Review'` | URL из `env` пустой (напр. `vac_report_url` на dev) → склеилось в `/Review` без хоста | заполнить нужный `*_URL` в `.env` либо положиться на skip |
| `500 No endpoint PUT /vaccination/Probe/NEW` | На dev лишний префикс `/vaccination` | на dev `DEV_BASE_URL` без префикса |
| `500 No endpoint ... /vac-report/...` | На dev обращаемся к vac-report по неверному адресу | узнать реальный host:port dev-сервиса, вписать в `DEV_VAC_REPORT_URL` |
| `AttributeError: 'dict' object has no attribute ...` | Обращение к `env` через точку | использовать `env["..."]` / `env.get("...")` |
| `401 Unauthorized` | Протух токен | обновить `*_TOKEN` в `.env` |
| `ConnectionError` / таймаут на dev | dev-хост доступен только из внутренней сети | подключиться к VPN/внутренней сети или гонять на test |
| Тесты `vac-report` все `SKIPPED` на dev | `DEV_VAC_REPORT_URL` пустой | это нормально; заполнить, если нужен прогон на dev |

---

## 9. Безопасность и гигиена репозитория (TODO для владельца репо)

Сейчас в публичном репозитории лежат `.env` с боевыми токенами и папка `__pycache__`. Это нужно поправить:

```bash
# 1. Создать .gitignore (см. ниже) и закоммитить
# 2. Убрать .env и кэш из индекса (файлы останутся локально)
git rm --cached .env
git rm -r --cached __pycache__ tests/__pycache__
git commit -m "chore: убрал .env и __pycache__ из репозитория"
git push
```

Рекомендуемый `.gitignore`:

```gitignore
# Окружение и секреты
.env

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# pytest / отчёты
.pytest_cache/
allure-results/
.coverage
htmlcov/
```

> Важно: токены, которые уже попали в публичную историю, считаются скомпрометированными. После чистки их стоит **перевыпустить** на стенде, а не просто удалить из файла. В репозитории должен оставаться только `.env.example` — с пустыми значениями токенов.

---

## 10. Быстрый старт (шпаргалка)

```bash
git clone https://github.com/babenkonikitos2004-cmd/autotest_bec.git
cd autotest_bec
python -m venv .venv && .venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
copy .env.example .env            # заполнить токены
git checkout -b fix/моя-задача
pytest --env=test -v              # прогнать
git add . && git commit -m "fix: ..." && git push -u origin fix/моя-задача
# → открыть Pull Request в main
```
