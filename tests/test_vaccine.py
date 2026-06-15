"""
Тесты: Выполненные прививки (Vaccine)
Конвертировано из Postman коллекции: проверка тестов вакцина
"""
import pytest
from datetime import date, timedelta

class TestVaccine:
    """CRUD тесты для выполненных прививок."""

    # ------------------------------------------------------------------ #
    #  PUT /Vaccine/NEW — создание выполненной прививки                   #
    # ------------------------------------------------------------------ #
    def test_create_executed_vaccine(self, api_client, env):
        """PUT /Vaccine/NEW — создание выполненной прививки."""
        today = date.today().isoformat()
        payload = {
            "patientId": "00000b30-c43a-423e-9260-d8f3798adddc",
            "docPerson": {
                "id":"6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8",
            },
            "createPerson": {
                "id":"6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
            },
            "nazDt":today,
            "createTm": today,
            "vacPrep": {
                "id": 415,
                "name": "Иммуноглобулин антирабический из сыворотки крови человека",
                "gtin": "312",
                "serial": "123",
                "manufacturer": None,
                "expirationDt": None,
                "doza": "13.000",
                "dozaInfo": "150 МЕ/мл",
                "unitId": "a0922ebc-c3e6-4453-b3c9-60b1b4ceb266",
                "unitName": None,
                "klpCode": "21.20.21.110-000012-1-00018-2000000807696",
                "islmpGuid": None,
                "paymentSource": None,
                "quantity": None,
            },
            "num": 13.000,
            "vacTourStr": "БЕШЕНСТВО (V6)",
            "medOrgId": "a8fad9fc-161e-4de9-adab-5ac32ae9c460",
            "introduction": {
                "id": "f755204b-499c-4c8f-911f-f7f5a89bd24b",
                "name": "Имплантация",
            },
            "payType": {
                "id": "3ab04a4c-5dc5-4e9a-b677-077a34d8ea6f",
                "name": "Средства обязательного медицинского страхования",
            },
            "isMultiTour": True,
            "indications": {
                "id": "5c3771e3-9322-499a-8407-d357fdc215ab",
                "name": "Иммунодиагностика",
            },
            "vaccinationTours": [
                {
                    "vacDiseaseId": 2,
                    "vacType": "Вакцинация",
                    "vacTypeId": 0,
                    "tour": "6",
                }
            ],
            "externalMo": False,
            "medOrg": "БУ \"НИЖНЕВАРТОВСКАЯ ОКРУЖНАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА\"",
            "externalPersonFio": None,
        "externalMoName": None,
        }

        response = api_client.put(f"{env['base_url']}/Vaccine/NEW", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"
        assert data["id"], "Поле 'id' пустое"

        env["created_vaccine_id"] = data["id"]

    # ------------------------------------------------------------------ #
    #  POST /Vaccine/{id} — редактирование выполненной прививки          #
    # ------------------------------------------------------------------ #
    def test_edit_executed_vaccine(self, api_client, env):
        """POST /Vaccine/{id} — редактирование выполненной прививки."""
        vaccine_id = env.get("created_vaccine_id")
        if not vaccine_id:
            pytest.skip("created_vaccine_id не задан — пропущен тест создания")
        today = date.today().isoformat()
        payload = {
            "patientId": "00000b30-c43a-423e-9260-d8f3798adddc",
            "docPerson": {
                "id":"6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8",
            },
            "createPerson": {
                "id":"6e9a7a9f-4eb3-4dd2-b23c-7564f7077ad8"
            },
            "nazDt":today,
            "createTm": today,
            "vacPrep": {
                "id": 415,
                "name": "Иммуноглобулин антирабический из сыворотки крови человека",
                "gtin": "312",
                "serial": "123",
                "manufacturer": None,
                "expirationDt": None,
                "doza": "13.000",
                "dozaInfo": "150 МЕ/мл",
                "unitId": "a0922ebc-c3e6-4453-b3c9-60b1b4ceb266",
                "unitName": None,
                "klpCode": "21.20.21.110-000012-1-00018-2000000807696",
                "islmpGuid": None,
                "paymentSource": None,
                "quantity": None,
            },
            "num": 13.000,
            "vacTourStr": "БЕШЕНСТВО (V6)",
            "medOrgId": "a8fad9fc-161e-4de9-adab-5ac32ae9c460",
            "introduction": {
                "id": "f755204b-499c-4c8f-911f-f7f5a89bd24b",
                "name": "Имплантация",
            },
            "payType": {
                "id": "3ab04a4c-5dc5-4e9a-b677-077a34d8ea6f",
                "name": "Средства обязательного медицинского страхования",
            },
            "isMultiTour": True,
            "indications": {
                "id": "5c3771e3-9322-499a-8407-d357fdc215ab",
                "name": "Иммунодиагностика",
            },
            "vaccinationTours": [
                {
                    "vacDiseaseId": 2,
                    "vacType": "Вакцинация",
                    "vacTypeId": 0,
                    "tour": "6",
                }
            ],
            "externalMo": False,
            "medOrg": "БУ \"НИЖНЕВАРТОВСКАЯ ОКРУЖНАЯ КЛИНИЧЕСКАЯ БОЛЬНИЦА\"",
            "externalPersonFio": None,
        "externalMoName": None,
        }

        response = api_client.post(
            f"{env['base_url']}/Vaccine/{vaccine_id}", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"

    # ------------------------------------------------------------------ #
    #  DELETE /Vaccine/{id} — удаление выполненной прививки              #
    # ------------------------------------------------------------------ #
    def test_delete_executed_vaccine(self, api_client, env):
        """DELETE /Vaccine/{id} — удаление выполненной прививки."""
        vaccine_id = env.get("created_vaccine_id")
        if not vaccine_id:
            pytest.skip("created_vaccine_id не задан — пропускаем DELETE")

        response = api_client.delete(f"{env['base_url']}/Vaccine/{vaccine_id}")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        # Проверяем время ответа
        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 6000, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 6000мс"
            )