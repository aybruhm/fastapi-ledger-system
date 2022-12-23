# FastAPI Imports
from fastapi import HTTPException, Depends

# Own Imports
from ledger.router import router
from core.deps import get_current_user
from models.user import User as UserModel
from ledger.services.operations import ledger_operations
from ledger.services.functions import (
    get_all_wallets_by_user,
    create_wallet as create_user_wallet,
)
from schemas.ledger import Wallet, WalletCreate, WalletDeposit, WalletWithdraw


@router.post("/wallets/", response_model=Wallet)
async def create_wallet(
    wallet: WalletCreate,
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.id != wallet.user:
        raise HTTPException(
            401, {"message": "Unauthorized to perform this action!"}
        )

    db_wallet = await create_user_wallet(wallet)
    return db_wallet


@router.get("/wallets/", response_model=list[Wallet])
async def get_wallets(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
):

    if current_user:
        db_wallets = await get_all_wallets_by_user(
            skip, limit, current_user.id
        )
        return db_wallets

    raise HTTPException(
        401, {"message": "Unauthorized to perform this action!"}
    )


@router.post("/deposit/")
async def deposit_money(
    deposit: WalletDeposit,
    current_user: UserModel = Depends(get_current_user),
) -> dict:

    if current_user.id != deposit.user:
        raise HTTPException(
            401, {"message": "Unauthorized to perform this action!"}
        )

    await ledger_operations.deposit_money_to_wallet(deposit)
    return {"message": f"NGN{deposit.amount} deposit successful!"}


@router.post("/withdraw/")
async def withdraw_money(
    withdraw: WalletWithdraw,
    current_user: UserModel = Depends(get_current_user),
) -> dict:

    if current_user.id != withdraw.user:
        raise HTTPException(
            401, {"message": "Unauthorized to perform this action!"}
        )

    await ledger_operations.withdraw_money_from_wallet(withdraw)
    return {"message": f"NGN{withdraw.amount} withdrawn successful!"}


@router.post("/transfer/wallet-to-wallet/")
async def wallet_to_wallet_transfer(
    wallet_from_id: int,
    withdraw: WalletWithdraw,
    current_user: UserModel = Depends(get_current_user),
) -> dict:

    if current_user.id != withdraw.user:
        raise HTTPException(
            401, {"message": "Unauthorized to perform this action!"}
        )

    await ledger_operations.withdraw_from_to_wallet_transfer(
        wallet_from_id, withdraw
    )
    return {
        "message": f"NGN{withdraw.amount} was transfered from \
            W#{wallet_from_id} wallet to W#{withdraw.id} wallet!"
    }


@router.post("/transfer/wallet-to-user/")
async def wallet_to_user_transfer(
    user_wallet: int,
    user_id: int,
    withdraw: WalletWithdraw,
    current_user: UserModel = Depends(get_current_user),
) -> dict:

    await ledger_operations.withdraw_from_to_user_wallet_transfer(
        user_id, user_wallet, withdraw
    )
    return {
        "message": f"Transferred NGN{withdraw.amount} \
            to U#{current_user.id} W#{user_wallet} wallet."
    }


@router.get("/balance/")
async def total_wallet_balance(
    current_user: UserModel = Depends(get_current_user),
) -> dict:

    balance = await ledger_operations.get_total_wallet_balance(current_user.id)
    return {"message": f"Total wallet balance is NGN{balance}"}


@router.get("/balance/wallet/")
async def wallet_balance(
    wallet_id: int,
    current_user: UserModel = Depends(get_current_user),
) -> dict:

    balance = await ledger_operations.get_wallet_balance(
        current_user.id, wallet_id
    )

    if balance is None:
        raise HTTPException(404, {"message": "Wallet does not exist!"})
    return {"message": f"Wallet balance is NGN{balance.amount}"}
