import requests
from django.conf import settings

def initiate_split_payment(email, total_amount, seller_subaccount, delivery_amount, order):
    total_amount = float(total_amount)
    delivery_amount = float(delivery_amount)

    # --- Breakdown in rands ---
    product_total = total_amount - delivery_amount - 4
    product_total_kobo = int(product_total * 100)
    delivery_kobo = int(4+delivery_amount * 100)
    grand_total_kobo = int(total_amount * 100)

    # --- Fixed platform cut ---
    platform_cut_kobo = 60  # R0.60 in kobo

    # Ensure we don’t assign more than available product value
    if product_total_kobo <= platform_cut_kobo:
        platform_cut_kobo = 0  # fallback, no split if value is too small

    seller_cut_kobo = product_total_kobo - platform_cut_kobo

    # --- Split by amount ---
    split_data = {
        "type": "flat",
        "bearer_type": "account",  # platform pays the Paystack fee
        "subaccounts": [
            {
                "subaccount": seller_subaccount,
                "share": seller_cut_kobo
            },
            # {
            #     "subaccount": settings.PAYSTACK_MAIN_ACCOUNT,
            #     "share": platform_cut_kobo
            # }
        ]
    }

    # --- Metadata for delivery ---
    metadata = {
        "order_id": order.id,
        "delivery_fee": delivery_kobo,
        "delivery_status": "pending",
        "future_courier_transfer": True
    }

    # --- Payload to Paystack ---
    payload = {
        "email": email,
        "amount": grand_total_kobo,  # product + delivery
        "split": split_data,
        "metadata": metadata
    }

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    # --- Make request ---
  

    response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
  
    if response.status_code == 200:
        data = response.json()["data"]
        order.ref = data['reference']
        order.save()
        return {
            "authorization_url": data["authorization_url"]
        }
    else:
        print("Payment error:", response.json())
        return None