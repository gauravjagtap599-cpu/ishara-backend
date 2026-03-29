from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from services.razorpay_service import create_order, verify_signature
from services.supabase_service import get_signed_url
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create order
@app.post("/create-order")
async def create_order_api(data: dict):
    order = create_order()
    return {
        "order_id": order["id"],
        "amount": order["amount"]
    }

# ✅ Verify payment
@app.post("/verify-payment")
async def verify_payment(data: dict):
    try:
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        print("VERIFY INPUT:", data)

        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            return {"error": "Missing payment data"}

        verify_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        subject_code = data.get("subject_code")
        file_name = f"{subject_code}.pdf"

        print("FILE:", file_name)

        # ✅ RETURN DOWNLOAD API (NOT SUPABASE URL)
        return {
            "download_url": f"http://127.0.0.1:8000/download?file_name={file_name}"
        }

    except Exception as e:
        print("VERIFY ERROR:", str(e))
        return {"error": "verification failed"}

# ✅ DOWNLOAD ROUTE (OUTSIDE)
@app.get("/download")
def download_file(file_name: str):
    file_url = f"https://ezmkkpicphlzkkyopzym.supabase.co/storage/v1/object/public/notes/{file_name}"

    response = requests.get(file_url, stream=True)

    return StreamingResponse(
        response.iter_content(chunk_size=1024),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={file_name}"
        }
    )