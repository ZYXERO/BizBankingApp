from fastapi import FastAPI

from api_service.controllers.account_controller import router as account_router
from api_service.controllers.customer_controller import router as customer_router
from api_service.data.store import InMemoryStore

# FastAPI validates JSON with type hints + Pydantic before our service layer runs.
app = FastAPI(title="BizBanking Backend API", version="1.0.0")

app.include_router(customer_router)
app.include_router(account_router)


@app.on_event("startup")
def startup_seed_data() -> None:
    InMemoryStore.seed_data()


@app.get("/")
def health() -> dict[str, str]:
    return {"message": "BizBanking Backend API is running"}
