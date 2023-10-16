import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def auth_headers():
    client = TestClient(app)

    response = client.post("/api/v1/store/user/create",
                            json={"name": "TESTname", "surname": "TESTsurname", "phone_number": "+71234567890",
                                  "password": "testpassword123"})

    response_data = response.json()

    token = response_data["token"]

    headers = {"Authorization": f"Bearer {token}"}
    return headers

class TestUser:
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_profile_user(self, auth_headers):
        response = self.client.get("/api/v1/store/user/profile", headers=auth_headers)
        assert response.status_code == 200

    def test_create_user_fail_phone_number(self):
        response = self.client.post("/api/v1/store/user/create",
                                   json={"name": "Failnumber", "surname": "Failnumber", "phone_number": "+71234",
                                         "password": "Failnumber123"})
        assert response.status_code == 400

    def test_update_user(self, auth_headers):
        response = self.client.put("/api/v1/store/user/update-profile", headers=auth_headers,
                                  json={"name": "newtest", "surname": "newtestsur", "phone_number": "+79178887767"})
        assert response.status_code == 200

