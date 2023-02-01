# Stdlib Imports
import json
import random
import string

# FastAPI Imports
from fastapi.testclient import TestClient

# Own Imports
from main import app
from orm.users import users_orm
from auth.hashers import pwd_hasher

# Third Party Imports
import pytest


# initialize test client
client = TestClient(app)


name = "".join(random.choice(string.ascii_lowercase) for i in range(6))
email = name + "@email.com"
password = name + "_weakpassword"


@pytest.mark.asyncio
async def test_create_user():
    """Ensure a user can register."""
    
    payload = {
        "name": name,
        "email": email,
        "password": password,
    }
    response = client.post("/register/", data=json.dumps(payload))

    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["is_active"] == True
    assert response.json()["wallets"] == []


@pytest.mark.asyncio
async def test_login_user_success():
    """Ensure a user can login successfully."""
    
    payload = {"email": email, "password": password}
    response = client.post("/login/", data=json.dumps(payload))

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_user_password_incorrect():
    """Ensure a user with incorrect password can not login."""
    
    payload = {"email": email, "password": "string"}
    response = client.post("/login/", data=json.dumps(payload))

    assert response.status_code == 401
    assert response.json()["detail"]["message"] == "Password incorrect!"


@pytest.mark.asyncio
async def test_login_user_password_not_exist():
    """Ensure a user that has no account can not login."""
    
    payload = {"email": "user@example.com", "password": "string"}
    response = client.post("/login/", data=json.dumps(payload))

    assert response.status_code == 404
    assert response.json()["detail"]["message"] == "User does not exist!"


@pytest.mark.asyncio
async def test_users_info():
    """Ensure an authenticated user with admin priviledges can get a list of users info."""

    # set up fake credentials for admin user
    admin_name = "".join(
        random.choice(string.ascii_lowercase) for i in range(8)
    )
    admin_email = admin_name + "@admin.com"
    admin_password = admin_name + "_weakpassword"
    admin_hashed_password = pwd_hasher.hash_password(
        admin_name + "_weakpassword"
    )

    # create fake admin user
    admin_user = await users_orm.create_admin(
        admin_name, admin_email, admin_hashed_password, True
    )

    login_response = client.post(
        "/login/",
        data=json.dumps(
            {"email": admin_user.email, "password": admin_password}
        ),
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/", headers={"Authorization": "Bearer " + token}
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_info():
    """Ensure an authenticated user can get their info."""

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
