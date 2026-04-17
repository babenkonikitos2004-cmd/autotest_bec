"""
Тесты: Паспорт участка — District
Конвертировано из Postman коллекции: проверка тестов паспорт Copy

Базовый URL: https://emis-test.miacugra.ru/district
Токен: из .env (TOKEN)
"""
import pytest

BASE_URL = "https://emis-test.miacugra.ru/district"

# Общий payload участка — базовые поля
_DISTRICT_BASE = {
    "departmentId": "fabe9ca9-025d-4a35-8658-eff26fa8036d",
    "departmentFrmoId": "667358b8-bccd-4086-8c10-1394d55c4d04",
    "moId": "0fe6e113-6bd0-4664-9718-d8a35e460a80",
    "attachmentTypeId": "8d69e7ef-9425-476b-8b5a-b94e9dc6ef71",
    "border": None,
    "endDt": None,
    "begAge": 21,
    "endAge": 60,
    "docPersonId": "164337c4-b982-4839-928e-1e8c812fe9f3",
    "docPersonEndDt": None,
    "substPersonId": "2749a994-5d7b-409e-b92f-e5f047298056",
    "substPersonEndDt": "2025-12-09",
    "nursePersonId": "164337c4-b982-4839-928e-1e8c812fe9f3",
    "nursePersonEndDt": None,
    "substNursePersonId": "12c6894e-096b-46a8-b0cb-801c7eb3642a",
    "countAll": 0,
    "countMan": 0,
    "countWoman": 0,
}


# ====================================================================== #
#  Создание участка                                                       #
# ====================================================================== #
class TestDistrictCreate:
    """Создание двух участков (нужны для теста объединения)."""

    def test_create_district_1(self, api_client, env):
        """PUT /District — создание участка 1."""
        payload = {
            **_DISTRICT_BASE,
            "name": "2434342444444444437",
            "begDt": "2025-11-12",
            "docPersonBegDt": "2025-11-12",
            "substPersonBegDt": "2025-11-30",
            "nursePersonBegDt": "2025-11-29",
            "substNursePersonBegDt": "2025-11-30",
            "substNursePersonEndDt": "2025-12-01",
        }

        response = api_client.put(f"{BASE_URL}/District", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"
        assert data["id"], "Поле 'id' пустое"

        env["created_district_id"] = data["id"]

    def test_create_district_2(self, api_client, env):
        """PUT /District — создание участка 2 (для объединения)."""
        payload = {
            **_DISTRICT_BASE,
            "name": "243434342432444",
            "begDt": "2025-11-17",
            "docPersonBegDt": "2025-11-17",
            "substPersonBegDt": "2025-11-30",
            "nursePersonBegDt": "2025-11-17",
            "substNursePersonBegDt": "2025-11-29",
            "substNursePersonEndDt": "2025-12-01",
        }

        response = api_client.put(f"{BASE_URL}/District", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"
        assert data["id"], "Поле 'id' пустое"

        env["created_district_id_2"] = data["id"]


# ====================================================================== #
#  Аналитическая панель                                                   #
# ====================================================================== #
class TestAnalysis:
    """Тесты аналитической панели участка."""

    MO_ID = "a8fad9fc-161e-4de9-adab-5ac32ae9c460"

    def test_get_analysis(self, api_client, env):
        """GET /Analysis?id={moId} — получение аналитической панели."""
        response = api_client.get(
            f"{BASE_URL}/Analysis", params={"id": self.MO_ID}
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

    def test_get_analysis_detail(self, api_client, env):
        """GET /Analysis?id={moId}&detail_type=ALL_COUNT — детализация."""
        mo_id = env.get("mo_id", self.MO_ID)

        response = api_client.get(
            f"{BASE_URL}/Analysis",
            params={"id": mo_id, "detail_type": "ALL_COUNT"},
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )


# ====================================================================== #
#  Редактирование и объединение участков                                  #
# ====================================================================== #
class TestDistrictEdit:
    """Редактирование, объединение и удаление участка."""

    def test_edit_district(self, api_client, env):
        """POST /District/{id} — редактирование участка."""
        district_id = env.get("created_district_id")
        if not district_id:
            pytest.skip("created_district_id не задан — пропущен тест создания")

        payload = {
            **_DISTRICT_BASE,
            "id": district_id,
            "name": "2991283",
            "begDt": "2025-10-07",
            "docPersonBegDt": "2025-10-02",
            "substPersonBegDt": "2025-10-30",
            "substPersonEndDt": "2025-11-09",
            "nursePersonBegDt": "2025-10-29",
            "substNursePersonBegDt": "2025-10-30",
            "substNursePersonEndDt": "2025-11-01",
        }

        response = api_client.post(
            f"{BASE_URL}/District/{district_id}", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert data.get("id") == district_id, (
            f"ID в ответе ({data.get('id')}) не совпадает с ожидаемым ({district_id})"
        )

    def test_merge_districts(self, api_client, env):
        """POST /District/{id1}/merge/{id2} — объединение двух участков."""
        district_id = env.get("created_district_id")
        district_id_2 = env.get("created_district_id_2")
        if not district_id or not district_id_2:
            pytest.skip("Один из district_id не задан — пропущены тесты создания")

        response = api_client.post(
            f"{BASE_URL}/District/{district_id}/merge/{district_id_2}"
        )

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

    def test_delete_district_2(self, api_client, env):
        """DELETE /District/{id2} — удаление участка 2 после объединения."""
        district_id_2 = env.get("created_district_id_2")
        if not district_id_2:
            pytest.skip("created_district_id_2 не задан")

        response = api_client.delete(f"{BASE_URL}/District/{district_id_2}")

        assert response.status_code in (200, 204, 404), (
            f"Ожидался статус 200/204/404, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )


# ====================================================================== #
#  Границы участка (Bounds)                                              #
# ====================================================================== #
class TestBounds:
    """CRUD тесты для границ участка."""

    def test_create_bound(self, api_client, env):
        """PUT /Bounds — добавление границы участка."""
        district_id = env.get("created_district_id")
        if not district_id:
            pytest.skip("created_district_id не задан")

        payload = {
            "districtId": district_id,
            "boundTypeId": "1f5ed5a8-4dfb-42ed-b780-73c9745ad28e",
            "boundTypeName": None,
            "addresses": [
                {
                    "id": "2d2f3be7-4777-46fd-a16c-0801cb25d504",
                    "addressType": "06be7db1-4331-4fb5-a855-c204cfec2d53",
                    "objectGuid": "04fbdbf7-a72f-405d-b7e8-ac959c5b16bb",
                    "kladrCode": "8600001100000300031",
                    "country": 171,
                    "countryName": "Россия",
                    "regionCode": "d66e5325-3a25-4d29-ba86-4ca351d9704b",
                    "regionName": "Ханты-Мансийский Автономный округ - Югра",
                    "regionType": "АО",
                    "areaCode": None,
                    "areaName": None,
                    "areaType": None,
                    "cityCode": "0bf0f4ed-13f8-446e-82f6-325498808076",
                    "cityName": "Нижневартовск",
                    "cityType": "г",
                    "settlementCode": None,
                    "settlementName": None,
                    "settlementType": None,
                    "localityCode": None,
                    "localityName": None,
                    "localityType": None,
                    "planningStructureCode": None,
                    "planningStructureName": None,
                    "planningStructureType": None,
                    "streetCode": "c765ffef-0964-47a1-b257-0892499978a4",
                    "streetName": "Ленина",
                    "streetType": "ул",
                    "houseCode": "ff388804-e3c9-4261-8659-1e8ab9a4d934",
                    "houseNum": "13",
                    "houseType": "д",
                    "okato": "71135000000",
                    "oktmo": "71875000001",
                    "flat": None,
                    "parkingCode": None,
                    "parkingNum": None,
                    "landPlotCode": None,
                    "landPlotNum": None,
                    "fullAddress": "Ханты-Мансийский Автономный округ - Югра, г Нижневартовск, ул Ленина, 13",
                }
            ],
        }

        response = api_client.put(f"{BASE_URL}/Bounds", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"
        assert data["id"], "Поле 'id' пустое"

        env["created_bound_id"] = data["id"]

    def test_edit_bound(self, api_client, env):
        """POST /Bounds/{id} — редактирование границы участка."""
        bound_id = env.get("created_bound_id")
        district_id = env.get("created_district_id")
        if not bound_id:
            pytest.skip("created_bound_id не задан — пропущен тест создания")

        payload = {
            "id": bound_id,
            "districtId": district_id,
            "boundTypeId": "34bea7ef-6d65-45d9-8780-11526478f2a6",
            "addresses": [
                {
                    "id": "ed171e72-bb71-4b36-8e57-c8f0c276d950",
                    "addressType": "06be7db1-4331-4fb5-a855-c204cfec2d53",
                    "objectGuid": "46b4c7e0-dbec-46b4-a6ed-e5907467aacc",
                    "kladrCode": "8600001100000300058",
                    "country": 171,
                    "countryName": "Россия",
                    "regionCode": "d66e5325-3a25-4d29-ba86-4ca351d9704b",
                    "regionName": "Ханты-Мансийский Автономный округ - Югра",
                    "regionType": "АО",
                    "areaCode": None,
                    "areaName": None,
                    "areaType": None,
                    "cityCode": "0bf0f4ed-13f8-446e-82f6-325498808076",
                    "cityName": "Нижневартовск",
                    "cityType": "г",
                    "planningStructureCode": None,
                    "planningStructureName": None,
                    "planningStructureType": None,
                    "streetCode": "c765ffef-0964-47a1-b257-0892499978a4",
                    "streetName": "Ленина",
                    "streetType": "ул",
                    "houseCode": "8e766130-2b7b-4b4d-8149-244ba6bb181f",
                    "houseNum": "15",
                    "houseType": "д",
                    "okato": "71135000000",
                    "oktmo": "71875000001",
                    "fullAddress": "Ханты-Мансийский Автономный округ - Югра, г Нижневартовск, ул Ленина, 15",
                }
            ],
        }

        response = api_client.post(f"{BASE_URL}/Bounds/{bound_id}", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert data.get("id") == bound_id, (
            f"ID в ответе ({data.get('id')}) не совпадает с ожидаемым ({bound_id})"
        )

    def test_delete_bound(self, api_client, env):
        """DELETE /Bounds/{id} — удаление границы участка."""
        bound_id = env.get("created_bound_id")
        if not bound_id:
            pytest.skip("created_bound_id не задан — пропущен тест создания")

        response = api_client.delete(f"{BASE_URL}/Bounds/{bound_id}")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 500, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 500мс"
            )


# ====================================================================== #
#  Профосмотры                                                            #
# ====================================================================== #
class TestProfOsmotr:
    """Тесты для работы с профосмотрами участка."""

    def test_get_prof_osmotr(self, api_client, env):
        """GET /prof/{districtId}/{type}/{year} — получение профосмотра."""
        district_id = env.get("created_district_id")
        if not district_id:
            pytest.skip("created_district_id не задан")

        response = api_client.get(f"{BASE_URL}/prof/{district_id}/1/2026")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )


# ====================================================================== #
#  Врачи участка (District/Doctor)                                        #
# ====================================================================== #
class TestDistrictDoctor:
    """CRUD тесты для врачей на участке."""

    def test_create_doctor(self, api_client, env):
        """PUT /District/Doctor — привязка врача к участку."""
        district_id = env.get("created_district_id")
        if not district_id:
            pytest.skip("created_district_id не задан")

        payload = {
            "districtId": district_id,
            "personId": "12c6894e-096b-46a8-b0cb-801c7eb3642a",
            "begDt": "2025-11-15",
            "endDt": "2025-11-20",
            "personName": None,
            "docTypeId": 2,
            "docTypeName": "Медсестра",
        }

        response = api_client.put(f"{BASE_URL}/District/Doctor", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"
        assert data["id"], "Поле 'id' пустое"

        env["created_doc_id"] = data["id"]

    def test_edit_doctor(self, api_client, env):
        """POST /District/Doctor — редактирование врача на участке."""
        doc_id = env.get("created_doc_id")
        district_id = env.get("created_district_id")
        if not doc_id:
            pytest.skip("created_doc_id не задан — пропущен тест создания")

        payload = {
            "id": doc_id,
            "districtId": district_id,
            "personId": "12c6894e-096b-46a8-b0cb-801c7eb3642a",
            "begDt": "2025-12-07",
            "endDt": "2025-12-14",
            "personName": None,
            "docTypeId": 4,
            "docTypeName": "Медсестра",
        }

        response = api_client.post(f"{BASE_URL}/District/Doctor", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

    def test_delete_doctor(self, api_client, env):
        """DELETE /District/Doctor/{id} — удаление врача с участка."""
        doc_id = env.get("created_doc_id")
        if not doc_id:
            pytest.skip("created_doc_id не задан — пропущен тест создания")

        response = api_client.delete(f"{BASE_URL}/District/Doctor/{doc_id}")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 500, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 500мс"
            )


# ====================================================================== #
#  Талоны (Dairy)                                                         #
# ====================================================================== #
_DAIRY_BASE = {
    "ser": "MOL",
    "num": "25",
    "dt": "2025-11-05",
    "patientId": "b7a01b4c-39d0-4a74-a3e2-a965d6fb3784",
    "patientFullName": "ПОГОРЕЛОВ АЛЕКСАНДР АЛЕКСАНДРОВИЧ М 05.09.1994 31 год",
    "privilegeCategoryId": "181ffb4e-fb95-49da-97b4-30c1aa4d4a11",
    "polisId": "fe3bfe85-d509-4459-9ba0-8995e20230c6",
    "personId": "a6e05b5a-3b19-4703-a584-4b2a99b86443",
    "districtId": "42d274de-c91d-4d7e-895f-2a1819a58388",
    "med": "88b0eb87-d728-4513-8ddd-aecfb6f7a2a4",
    "medName": None,
    "dosage": 12,
    "validity": "31f4ac36-03ba-4527-bdb4-ab0f0b831902",
    "dtd": None,
    "signa": "665",
    "signed": False,
    "signedECP": False,
    "statusISMLP": None,
}


class TestDairy:
    """CRUD тесты для талонов (Dairy)."""

    def test_create_dairy(self, api_client, env):
        """PUT /Dairy — создание талона."""
        payload = {**_DAIRY_BASE, "quantity": 110}

        response = api_client.put(f"{BASE_URL}/Dairy", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert "id" in data, f"Ответ не содержит поле 'id'. Получено: {list(data.keys())}"
        assert data["id"], "Поле 'id' пустое"

        env["created_deiry_id"] = data["id"]

    def test_edit_dairy(self, api_client, env):
        """POST /Dairy/{id} — редактирование талона."""
        dairy_id = env.get("created_deiry_id")
        if not dairy_id:
            pytest.skip("created_deiry_id не задан — пропущен тест создания")

        payload = {**_DAIRY_BASE, "id": dairy_id, "quantity": 150}

        response = api_client.post(f"{BASE_URL}/Dairy/{dairy_id}", json=payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert data.get("id") == dairy_id, (
            f"ID в ответе ({data.get('id')}) не совпадает с ожидаемым ({dairy_id})"
        )

    def test_sign_dairy(self, api_client, env):
        """POST /Dairy/{id}/sign — подпись талона."""
        dairy_id = env.get("created_deiry_id")
        if not dairy_id:
            pytest.skip("created_deiry_id не задан — пропущен тест создания")

        payload = {
            **_DAIRY_BASE,
            "id": dairy_id,
            "quantity": 150,
            "medName": "НАН 3 ОПТИПРО ,Сухие молочные напитки (стандартые) , 800 гр ",
        }

        response = api_client.post(
            f"{BASE_URL}/Dairy/{dairy_id}/sign", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        data = response.json()
        assert data.get("id") == dairy_id, (
            f"ID в ответе ({data.get('id')}) не совпадает с ожидаемым ({dairy_id})"
        )

    def test_unsign_dairy(self, api_client, env):
        """DELETE /Dairy/{id}/sign — снятие подписи с талона."""
        dairy_id = env.get("created_deiry_id")
        if not dairy_id:
            pytest.skip("created_deiry_id не задан — пропущен тест создания")

        payload = {
            **_DAIRY_BASE,
            "id": dairy_id,
            "quantity": 150,
            "medName": "НАН 3 ОПТИПРО ,Сухие молочные напитки (стандартые) , 800 гр ",
            "signed": True,
        }

        response = api_client.delete(
            f"{BASE_URL}/Dairy/{dairy_id}/sign", json=payload
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

    def test_delete_dairy(self, api_client, env):
        """DELETE /Dairy/{id} — удаление талона."""
        dairy_id = env.get("created_deiry_id")
        if not dairy_id:
            pytest.skip("created_deiry_id не задан — пропущен тест создания")

        response = api_client.delete(f"{BASE_URL}/Dairy/{dairy_id}")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 500, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 500мс"
            )


# ====================================================================== #
#  Финальное удаление участка 1                                           #
# ====================================================================== #
class TestDistrictDelete:
    """Финальное удаление основного участка."""

    def test_delete_district(self, api_client, env):
        """DELETE /District/{id} — удаление участка 1."""
        district_id = env.get("created_district_id")
        if not district_id:
            pytest.skip("created_district_id не задан")

        response = api_client.delete(f"{BASE_URL}/District/{district_id}")

        assert response.status_code in (200, 204), (
            f"Ожидался статус 200/204, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        if hasattr(response, "elapsed"):
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert elapsed_ms < 500, (
                f"Время ответа {elapsed_ms:.0f}мс превышает допустимые 500мс"
            )