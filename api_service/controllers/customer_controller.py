from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from api_service.models.schemas import CreateCustomerRequest, Customer, ErrorResponse, UpdateCustomerRequest
from api_service.services.customer_service import CustomerService

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("", response_model=list[Customer])
def get_all_customers() -> list[Customer]:
    return CustomerService.get_all_customers()


@router.get("/premium", response_model=list[Customer])
def get_all_premium_customers() -> list[Customer]:
    return CustomerService.get_all_premium_customers()


@router.get("/search", response_model=list[Customer])
def get_customer_by_name(name: str = Query(..., min_length=1)) -> list[Customer]:
    return CustomerService.search_customers_by_name(name)


@router.get("/{customer_id}", response_model=Customer, responses={404: {"model": ErrorResponse}})
def get_customer_by_id(customer_id: int) -> Customer:
    customer = CustomerService.get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.post("", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CreateCustomerRequest) -> Customer:
    return CustomerService.create_customer(payload)


@router.put("/{customer_id}", response_model=Customer, responses={404: {"model": ErrorResponse}})
def update_customer(customer_id: int, payload: UpdateCustomerRequest) -> Customer:
    customer = CustomerService.update_customer(customer_id, payload)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": ErrorResponse}})
def delete_customer(customer_id: int) -> None:
    deleted = CustomerService.delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
