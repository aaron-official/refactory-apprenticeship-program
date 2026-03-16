import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

logger = logging.getLogger(__name__)
router = APIRouter()
service = PaymentService(FakePaymentRepo())


@router.post("/customers", status_code=201)
async def create_customer(body: dict):
    name = body.get("name")
    email = body.get("email")

    if not name or not email:
        return JSONResponse(status_code=400, content={"error": "name and email are required"})
    if len(name) > 100:
        return JSONResponse(status_code=400, content={"error": "Name too long"})

    try:
        customer = service.create_customer(name, email)
        return JSONResponse(status_code=201, content=customer)
    except ValueError as e:
        msg = str(e)
        if "already exists" in msg:
            return JSONResponse(status_code=409, content={"error": msg})
        return JSONResponse(status_code=400, content={"error": msg})
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    customer = service.get_customer(customer_id)
    if not customer:
        return JSONResponse(status_code=404, content={"error": "Customer not found"})
    return customer


@router.get("/customers/{customer_id}/payments")
async def get_customer_payments(customer_id: str):
    customer = service.get_customer(customer_id)
    if not customer:
        return JSONResponse(status_code=404, content={"error": "Customer not found"})
    return service.get_payments_for_customer(customer_id)
