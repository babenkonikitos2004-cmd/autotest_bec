"""
Тесты: Медицинский отвод / отказ (Exemption)
Конвертировано из Postman коллекции: проверка тестов вакцина
"""
import pytest


_EXEMPTION_BASE = {
    "vacExemptionType": {"id": 1, "name": "Противопоказание"},
    "organizationId": "a8fad9fc-161e-4de9-adab-5ac32ae9c460",
    "indefinitePeriod": 1,
    "vacPrepAll": 0,
    "vacPrepId": 10154,
    "patientId": "b653f1e7-7f0d-4af0-b0cd-9df21f3a6718",
    "changeDt": "2025-10-30",
    "reason": {
        "id": "024907e4-16cf-49cf-aade-5aeb33391637",
        "name": "Все вакцины",
    },
    "icd10Id": [
        {
            "id": "45a65297-3999-4aa6-9a77-5fc85a7c3b4f",
            "name": "БОЛЕЗНИ НЕРВНОЙ СИСТЕМЫ",
        },
        {
            "id": "02ab04e8-9fdf-4e2e-ab9b-2aa788c72da3",
            "name": "БОЛЕЗНИ ГЛАЗА И ЕГО ПРИДАТОЧНОГО АППАРАТА",
        },
    ],
    "person": {
        "id": "a6e05b5a-3b19-4703-a584-4b2a99b86443",
        "name": "Круглов Петр Сергеевич",
    },
    "infectionDTO": [
        {"id": "", "infectionId": 5, "infectionName": "Брюшной тиф"}
    ],
}


class TestExemption:
    """CRUD тесты для медицинского отвода/отказа (Exemption)."""

    # ------------------------------------------------------------------ #
    #  PUT /Exemption/NEW — создание медотвода (своё МО)                  #
    # ------------------------------------------------------------------ #
    def test_create_exemption(self, api_client, env):
        """PUT /Exemption/NEW — создание медотвода в своём МО."""
        payload = {
            **_EXEMPTION_BASE,
            "begDt": "2025-11-28",
            "externalMo": False,
            "externalPersonFio": "null",
        }

        response = api_client.put(f"{env['base_url']}/Exemption/NEW", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, "Ответ не содержит поле 'id'"
        assert data["id"], "Поле 'id' пустое"

        env["created_medical_exemption_id"] = data["id"]

    # ------------------------------------------------------------------ #
    #  PUT /Exemption/NEW — создание медотвода (другое МО)               #
    # ------------------------------------------------------------------ #
    def test_create_exemption_external_mo(self, api_client, env):
        """PUT /Exemption/NEW — создание медотвода из другого МО."""
        payload = {
            **_EXEMPTION_BASE,
            "begDt": "2025-10-28",
            "externalMo": True,
            "externalMoName": "АбраКадабра",
            "externalPersonFio": "Горин Андрей",
        }

        response = api_client.put(f"{env['base_url']}/Exemption/NEW", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, "Ответ не содержит поле 'id'"
        assert data["id"], "Поле 'id' пустое"

        env["created_external_medical_exemption_id"] = data["id"]

    # ------------------------------------------------------------------ #
    #  POST /Exemption/{id} — редактирование медотвода                   #
    # ------------------------------------------------------------------ #
    def test_edit_exemption(self, api_client, env):
        """POST /Exemption/{id} — редактирование медотвода."""
        exemption_id = env.get("created_medical_exemption_id")
        if not exemption_id:
            pytest.skip("created_medical_exemption_id не задан — пропущен тест создания")

        payload = {
            "vacExemptionType": {"id": 1, "name": "Противопоказание"},
            "begDt": "2025-01-20",
            "endDt": None,
            "indefinitePeriod": 1,
            "vacPrepAll": 0,
            "vacPrepId": 10154,
            "organizationId": "a8fad9fc-161e-4de9-adab-5ac32ae9c460",
            "patientId": env.get(
                "patient_id", "b653f1e7-7f0d-4af0-b0cd-9df21f3a6718"
            ),
            "changeDt": "2025-10-28",
            "vacPrepGroup": None,
            "reason": {
                "id": "024907e4-16cf-49cf-aade-5aeb33391637",
                "name": "Все вакцины",
            },
            "reasonOther": None,
            "icd10Id": [
                {
                    "id": "45a65297-3999-4aa6-9a77-5fc85a7c3b4f",
                    "name": "БОЛЕЗНИ НЕРВНОЙ СИСТЕМЫ",
                },
                {
                    "id": "02ab04e8-9fdf-4e2e-ab9b-2aa788c72da3",
                    "name": "БОЛЕЗНИ ГЛАЗА И ЕГО ПРИДАТОЧНОГО АППАРАТА",
                },
            ],
            "infectionId": 5,
            "motivation": None,
            "person": {
                "id": "a6e05b5a-3b19-4703-a584-4b2a99b86443",
                "name": "Круглов Петр Сергеевич",
            },
        }

        response = api_client.post(
            f"{env['base_url']}/Exemption/{exemption_id}", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert data.get("id") == exemption_id, (
            f"ID в ответе ({data.get('id')}) не совпадает с ожидаемым ({exemption_id})"
        )

    # ------------------------------------------------------------------ #
    #  DELETE /Exemption/{id} — удаление медотвода (своё МО)             #
    # ------------------------------------------------------------------ #
    def test_delete_exemption(self, api_client, env):
        """DELETE /Exemption/{id} — удаление медотвода своего МО."""
        exemption_id = env.get("created_medical_exemption_id")
        if not exemption_id:
            pytest.skip("created_medical_exemption_id не задан — пропущен тест создания")

        response = api_client.delete(
            f"{env['base_url']}/Exemption/{exemption_id}"
        )

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

    # ------------------------------------------------------------------ #
    #  DELETE /Exemption/{id} — удаление медотвода (другое МО)           #
    # ------------------------------------------------------------------ #
    def test_delete_exemption_external_mo(self, api_client, env):
        """DELETE /Exemption/{id} — удаление медотвода внешнего МО."""
        exemption_id = env.get("created_external_medical_exemption_id")
        if not exemption_id:
            pytest.skip("created_external_medical_exemption_id не задан — пропущен тест создания")

        response = api_client.delete(
            f"{env['base_url']}/Exemption/{exemption_id}"
        )

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )