"""
Тесты: Работа со справочной информацией
  - File (vac-report/Review/File)
  - News (vac-report/News)
  - Review (vac-report/Review)
Конвертировано из Postman коллекции: проверка тестов вакцина
"""
import pytest

VAC_REPORT_URL = "https://emis-test.miacugra.ru/vac-report"


def _ensure_review_id(api_client, env):
    """
    Возвращает review_id из env (если уже создан) или создаёт новый обзор.
    Используется как в TestReviewFile, так и в TestReview,
    чтобы тесты не зависели от порядка запуска классов.
    """
    review_id = env.get("review_id")
    if review_id:
        return review_id

    resp = api_client.put(
        f"{VAC_REPORT_URL}/Review",
        json={"title": "Тестовый обзор (авто)", "reviewType": 0},
    )
    assert resp.status_code == 200, (
        f"Не удалось создать обзор для теста. "
        f"Статус: {resp.status_code}, тело: {resp.text}"
    )
    review_id = resp.json()["id"]
    env["review_id"] = review_id
    return review_id


# ====================================================================== #
#  File                                                                   #
# ====================================================================== #
class TestReviewFile:
    """Тесты для работы с файлами обзора (Review/File)."""

    def test_upload_review_file(self, api_client, env, tmp_path):
        """PUT /Review/File — загрузка файла к существующему обзору.

        Postman: form-data, поле 'data' типа File + query-params reviewId и Value.
        Время ответа ~938мс — лимит выставлен 2000мс (реальное время эндпоинта).
        """
        review_id = _ensure_review_id(api_client, env)

        # Параметры точно как в Postman: reviewId=<id>&Value (Value без значения)
        url = f"{VAC_REPORT_URL}/Review/File"
        params = {"reviewId": review_id, "Value": ""}

        # Убираем Content-Type из заголовков сессии —
        # requests сам выставит multipart/form-data с boundary
        headers = {"Content-Type": None}

        # Создаём временный PDF-подобный файл (сервер принимает любой файл)
        temp_file = tmp_path / "test_review.pdf"
        temp_file.write_bytes(b"%PDF-1.4 test content")

        with open(temp_file, "rb") as f:
            # Ключ поля — 'data' (как в Postman), тип application/pdf
            response = api_client.put(
                url,
                params=params,
                files={"data": (temp_file.name, f, "application/pdf")},
                headers=headers,
            )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        # Реальное время эндпоинта ~938мс, лимит 2000мс
        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 2000, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 2000мс"
            )

        try:
            data = response.json()
            if "id" in data:
                env["file_id"] = data["id"]
        except Exception:
            pass

    def test_get_review_file(self, api_client, env):
        """GET /Review/File?id={file_id} — получение файла обзора."""
        file_id = env.get("file_id")
        if not file_id:
            pytest.skip("file_id не задан — пропущен тест загрузки")

        response = api_client.get(
            f"{VAC_REPORT_URL}/Review/File",
            params={"id": file_id},
            headers={"Accept": "application/octet-stream"},
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 500

    def test_delete_review_file(self, api_client, env):
        """DELETE /Review/File?id={file_id} — удаление файла обзора."""
        file_id = env.get("file_id")
        if not file_id:
            pytest.skip("file_id не задан — пропущен тест загрузки")

        response = api_client.delete(
            f"{VAC_REPORT_URL}/Review/File", params={"id": file_id}
        )

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        env.pop("file_id", None)


# ====================================================================== #
#  News                                                                   #
# ====================================================================== #
class TestNews:
    """Тесты для работы с новостями (News)."""

    def test_create_or_edit_news(self, api_client, env):
        """PUT /News — создание/редактирование новости."""
        payload = {
            "title": "Тестовая новость",
            "description": "Описание тестовой новости",
            "createDt": "2025-12-03T06:54:06.463Z",
        }

        response = api_client.put(
            f"{VAC_REPORT_URL}/News",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"

        env["news_id"] = data["id"]

    def test_list_news(self, api_client, env):
        """POST /News — получение списка новостей."""
        payload = {
            "title": "string",
            "reviewType": 0,
            "page": {"pageNum": 0, "pageSize": 5000},
        }

        response = api_client.post(f"{VAC_REPORT_URL}/News", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, (
            f"Ожидался Content-Type application/json, получен: {content_type}"
        )

        data = response.json()
        assert isinstance(data, list), "Ответ должен быть массивом"

    def test_delete_news(self, api_client, env):
        """DELETE /News?id={news_id} — удаление новости."""
        news_id = env.get("news_id")
        if not news_id:
            pytest.skip("news_id не задан — пропущен тест создания")

        response = api_client.delete(
            f"{VAC_REPORT_URL}/News", params={"id": news_id}
        )

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        env.pop("news_id", None)


# ====================================================================== #
#  Review                                                                 #
# ====================================================================== #
class TestReview:
    """Тесты для работы с обзорами (Review)."""

    def test_create_review(self, api_client, env):
        """PUT /Review — создание обзора."""
        response = api_client.put(
            f"{VAC_REPORT_URL}/Review",
            json={"title": "Тестовый обзор", "reviewType": 0},
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"

        env["review_id"] = data["id"]

    def test_list_reviews(self, api_client, env):
        """POST /Review — получение списка обзоров."""
        payload = {
            "title": "string",
            "reviewType": 0,
            "page": {"pageNum": 0, "pageSize": 5000},
        }

        response = api_client.post(f"{VAC_REPORT_URL}/Review", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert isinstance(data, list), "Ответ должен быть массивом"

        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 2000, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 2000мс"
            )

    def test_delete_review(self, api_client, env):
        """DELETE /Review?id={review_id} — удаление обзора."""
        review_id = env.get("review_id")
        if not review_id:
            pytest.skip("review_id не задан — пропущен тест создания")

        response = api_client.delete(
            f"{VAC_REPORT_URL}/Review", params={"id": review_id}
        )

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        env.pop("review_id", None)