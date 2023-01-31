# Stdlib Imports
import json
import random
import string

# FastAPI Imports
from fastapi.testclient import TestClient

# Own Imports
from main import app
from core.deps import get_db
from orm.users import users_orm
from tests.conftest import _get_test_db, pytest


# override dependecy
app.dependency_overrides[get_db] = _get_test_db

# initialize test client
client = TestClient(app)


name = "".join(random.choice(string.ascii_lowercase) for i in range(6))
email = name + "@email.com"
password = name + "_weakpassword"


@pytest.mark.asyncio
async def test_create_user(create_tables):
    payload = {
        "name": "test user",
        "email": email,
        "password": password,
    }
    response = client.post("/register/", data=json.dumps(payload))

    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["is_active"] == True
    assert response.json()["wallets"] == []


@pytest.mark.asyncio
async def test_login_user_success(create_tables):
    payload = {"email": email, "password": password}
    response = client.post("/login/", data=json.dumps(payload))

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_user_password_incorrect(create_tables):
    payload = {"email": email, "password": "string"}
    response = client.post("/login/", data=json.dumps(payload))

    assert response.status_code == 401
    assert response.json()["detail"]["message"] == "Password incorrect!"


@pytest.mark.asyncio
async def test_login_user_password_not_exist(create_tables):
    payload = {"email": "user@example.com", "password": "string"}
    response = client.post("/login/", data=json.dumps(payload))

    assert response.status_code == 404
    assert response.json()["detail"]["message"] == "User does not exist!"


# @pytest.mark.asyncio
# async def test_users_info():

#     admin_user = await users_orm.create_admin(name, email, password, True)
#     login_response = client.post(
#         "/login/",
#         data=json.dumps({"email": admin_user.email, "password": password}),
#     )
#     token = login_response.json()["access_token"]

#     response = client.get(
#         "/users/", headers={"Authorization": "Bearer " + token}
#     )

#     assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_info(create_tables):

    login_response = client.post(
        "/login/", data=json.dumps({"email": email, "password": password})
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me/", headers={"Authorization": "Bearer " + token}
    )

    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["is_active"] == True
