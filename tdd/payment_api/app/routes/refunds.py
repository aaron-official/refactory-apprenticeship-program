"""app/routes/refunds.py"""
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

logger = logging.getLogger(__name__)
router = APIRouter()
service = PaymentService(FakePaymentRepo())


@router.post("/refunds", status_code=201)
async def create_refund(body: dict):
    payment_id = body.get("paymentId")
    amount = body.get("amount")

    if not payment_id or amount is None:
        return JSONResponse(status_code=400, content={"error": "paymentId and amount are required"})

    try:
        refund = service.refund(payment_id, amount)
        return JSONResponse(status_code=201, content=refund)
    except ValueError as e:
        msg = str(e)
        if "exceeds" in msg:
            return JSONResponse(status_code=422, content={"error": msg})
        if "not found" in msg.lower():
            return JSONResponse(status_code=404, content={"error": msg})
        return JSONResponse(status_code=400, content={"error": msg})
    except Exception as e:
        logger.error(e)
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})


@router.get("/refunds/{refund_id}")
async def get_refund(refund_id: str):
    refund = service.get_refund(refund_id)
    if not refund:
        return JSONResponse(status_code=404, content={"error": "Refund not found"})
    return refund
