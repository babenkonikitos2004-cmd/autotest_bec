"""
Тесты: Выполненные пробы
Конвертировано из Postman коллекции: проверка тестов вакцина
"""
import pytest
from datetime import date, timedelta

class TestProbe:
    """CRUD тесты для выполненных проб (Probe)."""

    # ------------------------------------------------------------------ #
    #  PUT /Probe/NEW — создание выполненной пробы                        #
    # ------------------------------------------------------------------ #
    def test_create_executed_probe(self, api_client, env):
        """PUT /Probe/NEW — успешное создание выполненной пробы."""
        today = date.today().isoformat()
        payload = {
             "patientId": "00000b30-c43a-423e-9260-d8f3798adddc",
    "medOrg": "БУ \"НИЖНЕВАРТОВСКАЯ ОКРУЖНАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА\"",
    "medOrgId": "a8fad9fc-161e-4de9-adab-5ac32ae9c460",
    "moCheckbox":[],
    "docPerson": {
        "id": "6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
    },
    "insertPosition": {
        "id": "6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
    },
    "createPerson": {
        "id": "6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
    },
            "createDt": today,
            "executeDt": today,
             "vacPrep": {
        "id": 111727,
        "name": "ЭпиВакКорона Вакцина на основе пептидных антигенов для профилактики COVID-19",
        "gtin": "13231",
        "serial": "3232",
        "manufacturer": None,
                "expirationDt": (date.today() + timedelta(days=365)).isoformat(),
                "doza": "1.000",
                "dozaInfo": None,
                "unitId": "74108900-9877-4762-b528-bcfb89546be2",
                "unitName": None,
                "klpCode": None,
                "islmpGuid": None,
                "paymentSource": None,
                "quantity": None,
            },
            "introduction": {
        "id": "e22ca6b5-2820-4425-a8d2-7f6f9dff2b07",
        "name": "Инфильтрация"
    },
    "introductionPlace": None,
    "payType": {
        "id": "57369a94-c43b-4afb-85c8-8bab9e451971",
        "name": "Средства третьих юридических лиц"
    },
    "result": {
        "id": 2,
        "name": "Сомнительная"
    },
    "num":"1.000",
    "papulaSize": "5",
    "rem": None,
    "infection": "Туберкулез",
    "reactions": [],
    "vacProbePlanId": None,
    "historical": False,
    "drugBalanceUse": False,
    "islmpDrugDiscarded": None,
    "sign": 0,
   "nazDt":"2026-06-15",
    "vacProbeType": {
        "id": "2bc01668-7408-11ef-9e27-080027edb999",
        "name": "Проба Манту"
    }
}

        response = api_client.put(f"{env['base_url']}/Probe/NEW", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, "Ответ не содержит поле 'id'"
        assert data["id"], "Поле 'id' пустое"

        env["created_executed_probe_id"] = data["id"]

    # ------------------------------------------------------------------ #
    #  POST /Probe/{id} — редактирование выполненной пробы               #
    # ------------------------------------------------------------------ #
    def test_edit_executed_probe(self, api_client, env):
        """POST /Probe/{id} — редактирование выполненной пробы."""
        probe_id = env.get("created_executed_probe_id")
        if not probe_id:
            pytest.skip("created_executed_probe_id не задан — пропущен тест создания")
        today = date.today().isoformat()

        payload = {
            "patientId": env.get("patient_id", "00000b30-c43a-423e-9260-d8f3798adddc"),
             "medOrg": "БУ \"НИЖНЕВАРТОВСКАЯ ОКРУЖНАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА\"",
    "medOrgId": "a8fad9fc-161e-4de9-adab-5ac32ae9c460",
    "moCheckbox":[],
    "docPerson": {
        "id": "6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
    },
    "insertPosition": {
        "id": "6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
    },
    "createPerson": {
        "id": "6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
    },
            "createDt": today,
            "executeDt": today ,
            "vacPrep": {
                "id": 111727,
                "name": "ЭпиВакКорона Вакцина на основе пептидных антигенов для профилактики COVID-19",
                "gtin": "13231",
                "serial": "3232",
                "manufacturer": None,
                "expirationDt": (date.today() + timedelta(days=365)).isoformat(),
                "doza": "1.000",
                "dozaInfo": None,
                "unitId": "74108900-9877-4762-b528-bcfb89546be2",
                "unitName": None,
                "klpCode": None,
                "islmpGuid": None,
                "paymentSource": None,
                "quantity": None,
            },
            "introduction": {
        "id": "e22ca6b5-2820-4425-a8d2-7f6f9dff2b07",
        "name": "Инфильтрация"
    },
    "introductionPlace": None,
    "payType": {
        "id": "57369a94-c43b-4afb-85c8-8bab9e451971",
        "name": "Средства третьих юридических лиц"
    },
    "result": {
        "id": 2,
        "name": "Сомнительная"
    },
    "num":"3.000",
    "papulaSize": "5",
    "rem": None,
    "infection": "Туберкулез",
    "reactions": [],
    "vacProbePlanId": None,
    "historical": False,
    "drugBalanceUse": False,
    "islmpDrugDiscarded": None,
    "sign": 0,
   "nazDt":"2026-06-15",
    "vacProbeType": {
        "id": "2bc01668-7408-11ef-9e27-080027edb999",
        "name": "Проба Манту"
    }

}

        response = api_client.post(
            f"{env['base_url']}/Probe/{probe_id}", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, "Ответ не содержит поле 'id'"

    # ------------------------------------------------------------------ #к
    #  DELETE /Probe/{id} — удаление выполненной пробы                   #
    # ------------------------------------------------------------------ #
    def test_delete_executed_probe(self, api_client, env):
        """DELETE /Probe/{id} — удаление выполненной пробы."""
        probe_id = env.get("created_executed_probe_id")
        if not probe_id:
            pytest.skip("created_executed_probe_id не задан — пропущен тест создания")

        response = api_client.delete(f"{env['base_url']}/Probe/{probe_id}")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )