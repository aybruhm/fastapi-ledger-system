# Stdlib Imports
import json
import random
import string
from typing import Tuple

# Own Imports
from orm.users import users_orm
from orm.ledger import ledger_orm
from tests.test_user import client

# Third Party Imports
import pytest


name = "".join(random.choice(string.ascii_lowercase) for i in range(6))
email = name + "@email.com"
password = name + "_weakpassword"

wallet_title = "".join(random.choice(string.ascii_lowercase) for i in range(6))


async def create_user() -> Tuple[dict, str]:
    """Function to create a user."""

    payload = {"name": name, "email": email, "password": password}
    response = client.post("/register/", data=json.dumps(payload))
    return response.json(), password


async def login_user(u_email: str, u_password: str):
    """Function to login a user and get the access token."""

    payload = {"email": u_email, "password": u_password}
    response = client.post("/login/", data=json.dumps(payload))
    return response.json()["access_token"]


async def get_user_id(u_email: str) -> int:
    """Function to get the user id."""

    user = await users_orm.get_email(u_email)
    return user.id


@pytest.mark.asyncio
async def test_create_wallet():
    """Ensure an authenticated user can create a wallet."""

    user, u_password = await create_user()
    token = await login_user(user["email"], u_password)
    user_id = await get_user_id(user["email"])

    payload = {
        "user": user_id,
        "amount": random.randint(10000, 99999),
        "title": wallet_title,
    }
    response = client.post(
        "/wallets/",
        data=json.dumps(payload),
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
    assert response.json()["user"] == user_id
    assert response.json()["title"] == wallet_title


@pytest.mark.asyncio
async def test_get_wallets():
    """Ensure an authenticated user can get their wallets."""

    token = await login_user(email, password)
    response = client.get(
        "/wallets/", headers={"Authorization": "Bearer " + token}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_deposit_money():
    """Ensure an authenticated user can deposit money."""

    user_id = await get_user_id(email)
    token = await login_user(email, password)
    wallets = await ledger_orm.filter(
        **{"user_id": user_id, "skip": 0, "limit": 2}
    )

    payload = {"user": user_id, "amount": 5000, "id": wallets[0].id}
    response = client.post(
        "/deposit/",
        data=json.dumps(payload),
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == f"NGN{payload['amount']} deposit successful!"
    )


@pytest.mark.asyncio
async def test_withdraw_money():
    """Ensure an authenticated user can withdraw money."""

    user_id = await get_user_id(email)
    token = await login_user(email, password)
    wallets = await ledger_orm.filter(
        **{"user_id": user_id, "skip": 0, "limit": 2}
    )

    payload = {"user": user_id, "amount": 5000, "id": wallets[0].id}
    response = client.post(
        "/withdraw/",
        data=json.dumps(payload),
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == f"NGN{payload['amount']} withdrawn successful!"
    )


@pytest.mark.asyncio
async def test_wallet_to_wallet_transfer():
    """Ensure an authenticated user can transfer from x to y wallet."""

    user_id = await get_user_id(email)
    token = await login_user(email, password)

    wallet_from = client.post(
        "/wallets/",
        data=json.dumps(
            {
                "user": user_id,
                "amount": random.randint(10000, 99999),
                "title": wallet_title,
            }
        ),
        headers={"Authorization": "Bearer " + token},
    )
    wallet_to = client.post(
        "/wallets/",
        data=json.dumps(
            {
                "user": user_id,
                "amount": random.randint(10000, 99999),
                "title": wallet_title + "_2",
            }
        ),
        headers={"Authorization": "Bearer " + token},
    )

    payload = {
        "user": user_id,
        "amount": 50000,
        "wallet_from": wallet_from.json()["id"],
        "wallet_to": wallet_to.json()["id"],
    }
    response = client.post(
        "/transfer/wallet-to-wallet/",
        data=json.dumps(payload),
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == f"NGN{payload['amount']} was transfered from \
            W#{wallet_from.json()['id']} wallet to W#{wallet_to.json()['id']} wallet!"
    )


@pytest.mark.asyncio
async def test_wallet_to_user_transfer():
    """Ensure an authenticated user can transfer their account to
    another user's account."""

    user_id = await get_user_id(email)
    token = await login_user(email, password)

    r_user_name = "".join(
        random.choice(string.ascii_lowercase) for i in range(6)
    )
    r_user_email = r_user_name + "@email.com"
    r_user_password = r_user_name + "_weakpassword"

    receiving_user = client.post(
        "/register/",
        data=json.dumps(
            {
                "name": r_user_name,
                "email": r_user_email,
                "password": r_user_password,
            }
        ),
    )
    receiving_user_token = await login_user(r_user_email, r_user_password)

    wallet_from = client.post(
        "/wallets/",
        data=json.dumps(
            {
                "user": user_id,
                "amount": random.randint(10000, 99999),
                "title": wallet_title,
            }
        ),
        headers={"Authorization": "Bearer " + token},
    )
    wallet_to = client.post(
        "/wallets/",
        data=json.dumps(
            {
                "user": receiving_user.json()["id"],
                "amount": random.randint(10000, 99999),
                "title": wallet_title + "_2",
            }
        ),
        headers={"Authorization": "Bearer " + receiving_user_token},
    )

    payload = {
        "user": user_id,
        "amount": 3000,
        "wallet_from": wallet_from.json()["id"],
        "wallet_to": wallet_to.json()["id"],
        "user_to": receiving_user.json()["id"],
    }
    response = client.post(
        "/transfer/wallet-to-user/",
        data=json.dumps(payload),
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
    assert wallet_from.status_code == 200
    assert wallet_to.status_code == 200

    assert (
        response.json()["message"]
        == f"Transferred NGN{payload['amount']} \
            to U#{receiving_user.json()['id']} W#{wallet_to.json()['id']} wallet."
    )
    assert wallet_from.json()["user"] == user_id
    assert wallet_from.json()["title"] == wallet_title
    assert wallet_to.json()["user"] == receiving_user.json()["id"]
    assert wallet_to.json()["title"] == wallet_title + "_2"


@pytest.mark.asyncio
async def test_total_wallet_balance():
    """Ensure an authenticated user can get the total balance of their wallets."""

    token = await login_user(email, password)
    response = client.get(
        "/balance/", headers={"Authorization": "Bearer " + token}
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_wallet_balance():
    """Ensure an authenticated user can get the balance of a particular wallet."""

    token = await login_user(email, password)
    user_id = await get_user_id(email)
    wallets = await ledger_orm.filter(
        **{"user_id": user_id, "skip": 0, "limit": 2}
    )

    response = client.get(
        "/balance/",
        params={"wallet_id": wallets[0].id},
        headers={"Authorization": "Bearer " + token},
    )

    assert response.status_code == 200
