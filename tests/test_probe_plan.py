"""
Тесты: Запланированные пробы
Конвертировано из Postman коллекции: проверка тестов вакцина
"""
import pytest
import requests


class TestProbePlan:
    """
    CRUD тесты для запланированных проб (ProbePlan).
    Порядок выполнения важен: create → edit → delete.
    ID созданной записи передаётся через фикстуру session-scope.
    """

    # ------------------------------------------------------------------ #
    #  PUT /ProbePlan/NEW — создание                                       #
    # ------------------------------------------------------------------ #
    def test_create_probe_plan(self, api_client, env):
        """PUT /ProbePlan/NEW — успешное создание запланированной пробы."""
        payload = {
            "patientId": "00000b30-c43a-423e-9260-d8f3798adddc",
            "vacProbeId": None ,
            "vacProbeTypeId": "2bc01668-7408-11ef-9e27-080027edb999",
            "vacPlanStatusId": 5,
            "nazPersonId": "a6e05b5a-3b19-4703-a584-4b2a99b86443",
            "planDt": "2025-10-31",
        }

        response = api_client.put(f"{env['base_url']}/ProbePlan/NEW", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, "Ответ не содержит поле 'id'"
        assert data["id"], "Поле 'id' пустое"

        # Сохраняем ID для последующих шагов
        env["created_probe_id"] = data["id"]

    # ------------------------------------------------------------------ #
    #  POST /ProbePlan/{id} — редактирование                              #
    # ------------------------------------------------------------------ #
    def test_edit_probe_plan(self, api_client, env):
        """POST /ProbePlan/{id} — редактирование запланированной пробы."""
        probe_id = env.get("created_probe_id")
        if not probe_id:
            pytest.skip("created_probe_id не задан — пропущен тест создания")

        payload = {
            "patientId": env.get("patient_id", "00000b30-c43a-423e-9260-d8f3798adddc"),
            "vacProbeId": None,
            "vacProbeTypeId": "2bc01668-7408-11ef-9e27-080027edb999",
            "vacPlanStatusId": 5,
            "nazPersonId": "a6e05b5a-3b19-4703-a584-4b2a99b86443",
            "planDt": "2025-12-31",
        }

        response = api_client.post(
            f"{env['base_url']}/ProbePlan/{probe_id}", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert data.get("id") == probe_id, (
            f"ID в ответе ({data.get('id')}) не совпадает с ожидаемым ({probe_id})"
        )

    # ------------------------------------------------------------------ #
    #  DELETE /ProbePlan/{id} — удаление                                  #
    # ------------------------------------------------------------------ #
    def test_delete_probe_plan(self, api_client, env):
        """DELETE /ProbePlan/{id} — удаление запланированной пробы."""
        probe_id = env.get("created_probe_id")
        if not probe_id:
            pytest.skip("created_probe_id не задан — пропущен тест создания")

        response = api_client.delete(f"{env['base_url']}/ProbePlan/{probe_id}")

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )