from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from api_service.models.schemas import Account, CreateAccountRequest, ErrorResponse, UpdateAccountRequest
from api_service.services.account_service import AccountService

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.get("", response_model=list[Account])
def get_all_accounts() -> list[Account]:
    return AccountService.get_all_accounts()


@router.get("/search", response_model=list[Account])
def get_accounts_by_name(name: str = Query(..., min_length=1)) -> list[Account]:
    return AccountService.search_accounts_by_customer_name(name)


@router.get("/{account_id}", response_model=Account, responses={404: {"model": ErrorResponse}})
def get_account_by_id(account_id: int) -> Account:
    account = AccountService.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@router.post("", response_model=Account, status_code=status.HTTP_201_CREATED, responses={404: {"model": ErrorResponse}})
def create_account(payload: CreateAccountRequest) -> Account:
    account = AccountService.create_account(payload)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return account


@router.put("/{account_id}", response_model=Account, responses={404: {"model": ErrorResponse}})
def update_account(account_id: int, payload: UpdateAccountRequest) -> Account:
    account = AccountService.update_account(account_id, payload)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account or customer not found")
    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": ErrorResponse}})
def delete_account(account_id: int) -> None:
    deleted = AccountService.delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
