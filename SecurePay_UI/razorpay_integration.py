
import razorpay

def create_order(amount):
    client = razorpay.Client(auth=("Your_API_NAME", "Your_API_KEY"))

    data = {
        "amount": amount,  # Amount in paise (e.g., 1999 = ₹19.99)
        "currency": "INR",
        "payment_capture": 1  # Auto-capture payment
    }

    try:
        order = client.order.create(data=data)
        return order
    except Exception as e:
        print(f"Error creating order: {e}")
        return None
