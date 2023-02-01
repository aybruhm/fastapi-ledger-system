# Own Imports
from tests.test_user import client

# Third Party Imports
import pytest


async def login_user():
    """Function to login a user and get the access token."""
    pass


@pytest.mark.asyncio
async def test_create_wallet():
    """Ensure a user can create a wallet."""
    pass


@pytest.mark.asyncio
async def test_get_wallets():
    """Ensure an authenticated user can get their wallets."""
    pass


@pytest.mark.asyncio
async def test_deposit_money():
    """Ensure an authenticated user can deposit money."""
    pass


@pytest.mark.asyncio
async def test_withdraw_money():
    """Ensure an authenticated user can withdraw money."""
    pass


@pytest.mark.asyncio
async def test_wallet_to_wallet_transfer():
    """Ensure an authenticated user can transfer from x to y wallet."""
    pass


@pytest.mark.asyncio
async def test_wallet_to_user_transfer():
    """Ensure an authenticated user can transfer his their account to
    another user's account."""
    pass


@pytest.mark.asyncio
async def test_total_wallet_balance():
    """Ensure an authenticated user can get the total balance of their wallets."""
    pass


@pytest.mark.asyncio
async def test_wallet_balance():
    """Ensure an authenticated user can get the balance of a particular wallet."""
    pass
