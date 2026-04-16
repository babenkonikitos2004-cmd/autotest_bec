"""
Тесты: Запланированные прививки (Vaccine/plan)
Конвертировано из Postman коллекции: проверка тестов вакцина
"""
import pytest


class TestVaccinePlan:
    """CRUD тесты для запланированных прививок."""

    # ------------------------------------------------------------------ #
    #  PUT /Vaccine/plan/NEW — создание запланированной прививки          #
    # ------------------------------------------------------------------ #
    def test_create_vaccine_plan(self, api_client, env):
        """PUT /Vaccine/plan/NEW — создание запланированной прививки."""
        payload = {
            "patientId": "00000b30-c43a-423e-9260-d8f3798adddc",
            "planDt": "2025-10-28",
            "anamnezDt": "2025-07-20",
            "indicationsUse": {
                "id": "24a00e44-3eb0-4076-a940-481f393b3d00",
                "name": "Иные",
            },
            "vacDisease": {"id": "4", "name": "Дифтерия"},
            "vacType": {"id": "2", "name": "Дополнительная иммунизация"},
            "tour": "4",
            "nazPerson": {
                "id": "f18e2464-3864-4720-8077-0936cb668c79",
                "name": "Лихачева Ирина Сергеевна",
            },
            "vacPlanStatus": {
                "id": 5,
                "name": "План ручн"
            },
        }

        response = api_client.put(f"{env['base_url']}/Vaccine/plan/NEW", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, "Ответ не содержит поле 'id'"
        assert data["id"], "Поле 'id' пустое"

        env["created_vaccine_plan_id"] = data["id"]

    # ------------------------------------------------------------------ #
    #  POST /Vaccine/plan/{id} — редактирование                          #
    # ------------------------------------------------------------------ #
    def test_edit_vaccine_plan(self, api_client, env):
        """POST /Vaccine/plan/{id} — редактирование запланированной прививки."""
        plan_id = env.get("created_vaccine_plan_id")
        if not plan_id:
            pytest.skip("created_vaccine_plan_id не задан — пропущен тест создания")

        payload = {
            "id": plan_id,
            "patientId": "00000b30-c43a-423e-9260-d8f3798adddc",
            "planDt": "2025-08-04",
            "anamnezDt": "2025-07-20",
            "schema": None,
            "indicationsUse": {
                "id": "24a00e44-3eb0-4076-a940-481f393b3d00",
                "name": "Иные",
            },
            "vacDisease": {"id": 6, "name": "Дифтерия"},
            "vacType": {"id": 2, "name": "Дополнительная иммунизация"},
            "vaccinationId": None,
            "tour": "4",
            "vacPlanStatus": {"id": 5, "name": "План ручн"},
            "executeDt": None,
            "nazPerson": {
                "id": "f18e2464-3864-4720-8077-0936cb668c79",
                "name": "Лихачева Ирина Сергеевна",
            },
            "comment": None,
        }

        response = api_client.post(
            f"{env['base_url']}/Vaccine/plan/{plan_id}", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert data.get("id") == plan_id, (
            f"ID в ответе ({data.get('id')}) не совпадает с ожидаемым ({plan_id})"
        )

    # ------------------------------------------------------------------ #
    #  POST /Vaccine/CustomPlan/Calc — кастомный план                    #
    # ------------------------------------------------------------------ #
    def test_create_custom_vaccine_plan(self, api_client, env):
        """POST /Vaccine/CustomPlan/Calc — создание кастомного плана прививок."""
        payload = {"patientIds": ["00014cf0-1b18-421f-a4b4-b2ed684d3c03"]}

        response = api_client.post(
            f"{env['base_url']}/Vaccine/CustomPlan/Calc", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        # Ответ должен быть числом
        try:
            result = int(response.text.strip())
        except ValueError:
            pytest.fail(
                f"Ожидалось числовое значение в теле ответа, получено: {response.text}"
            )
        assert isinstance(result, int), "Ответ не является целым числом"

    # ------------------------------------------------------------------ #
    #  DELETE /Vaccine/plan/{id} — удаление                              #
    # ------------------------------------------------------------------ #
    def test_delete_vaccine_plan(self, api_client, env):
        """DELETE /Vaccine/plan/{id} — удаление запланированной прививки."""
        plan_id = env.get("created_vaccine_plan_id")
        if not plan_id:
            pytest.skip("created_vaccine_plan_id не задан — пропускаем DELETE")

        response = api_client.delete(f"{env['base_url']}/Vaccine/plan/{plan_id}")

        assert response.status_code in (200, 204, 404), (
            f"Ожидался статус 200/204/404, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        # Проверяем время ответа (если доступно в объекте response)
        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 5000, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 5000мс"
            )