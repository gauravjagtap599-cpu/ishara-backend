import razorpay

RAZORPAY_KEY_ID = "rzp_live_SWvOMpWLlFdERR"
RAZORPAY_SECRET = "Jv4r1zkTNAlf0914Kvuw3ftn"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))

def create_order():
    return client.order.create({
        "amount": 2000,
        "currency": "INR",
        "payment_capture": 1
    })

def verify_signature(data):
    client.utility.verify_payment_signature(data)