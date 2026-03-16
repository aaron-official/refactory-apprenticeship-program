import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

logger = logging.getLogger(__name__)
router = APIRouter()
service = PaymentService(FakePaymentRepo())


@router.post("/payments", status_code=201)
async def create_payment(body: dict | None = None):
    if not body:
        return JSONResponse(status_code=400, content={"error": "Request body required"})

    customer_id = body.get("customerId")
    amount = body.get("amount")
    currency = body.get("currency")

    if customer_id is None or amount is None or currency is None:
        return JSONResponse(status_code=400, content={"error": "customerId, amount and currency are required"})
    if not currency:
        return JSONResponse(status_code=400, content={"error": "Invalid currency"})

    try:
        payment = service.create_payment(customer_id, amount, currency)
        return JSONResponse(status_code=201, content=payment)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})


@router.get("/payments")
async def get_payments():
    try:
        return service.get_all_payments()
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})


@router.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    payment = service.get_payment(payment_id)
    if not payment:
        return JSONResponse(status_code=404, content={"error": "Payment not found"})
    return payment


@router.post("/payments/{payment_id}/capture")
async def capture_payment(payment_id: str):
    try:
        payment = service.capture(payment_id)
        return payment
    except ValueError as e:
        msg = str(e)
        if "not found" in msg.lower():
            return JSONResponse(status_code=404, content={"error": msg})
        return JSONResponse(status_code=409, content={"error": msg})
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})


@router.post("/payments/{payment_id}/fail")
async def fail_payment(payment_id: str):
    try:
        payment = service.fail(payment_id)
        return payment
    except ValueError as e:
        msg = str(e)
        if "not found" in msg.lower():
            return JSONResponse(status_code=404, content={"error": msg})
        return JSONResponse(status_code=409, content={"error": msg})
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})
