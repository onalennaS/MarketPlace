import requests
from django.conf import settings

def initiate_split_payment(email, total_amount, seller_subaccount, delivery_amount, order):
    # Ensure proper types
    total_amount = float(total_amount)
    delivery_amount = float(delivery_amount)

    # Breakdown amounts
    product_total = total_amount - delivery_amount
    product_total_kobo = int(product_total * 100)
    delivery_kobo = int(delivery_amount * 100)
    grand_total_kobo = int(total_amount * 100)

    # --- Platform cut calculation ---
    platform_flat_fee_rands = 4  # R4 platform fee
    estimated_paystack_fee = (product_total * 2.9 / 100) + 1  # Paystack's cut
    expected_platform_cut = platform_flat_fee_rands - estimated_paystack_fee

    if expected_platform_cut < 0:
        expected_platform_cut = 0

    # Convert to percentage of product_total
    platform_percentage = (expected_platform_cut / product_total) * 100 if product_total > 0 else 0
    seller_percentage = 100 - platform_percentage

    # --- Split rule for product only ---
    split_data = {
        "type": "percentage",
        "bearer_type": "account",
        "subaccounts": [
            {
                "subaccount": seller_subaccount,
                "share": seller_percentage
            },
            {
                "subaccount": settings.PAYSTACK_MAIN_ACCOUNT,
                "share": platform_percentage
            }
        ]
    }

    # --- Metadata for delivery logic ---
    metadata = {
        "order_id": order.id,
        "delivery_fee": delivery_kobo,
        "delivery_status": "pending",
        "future_courier_transfer": True
    }

    # --- Paystack Payload ---
    payload = {
        "email": email,
        "amount": grand_total_kobo,
        "split": split_data,
        "metadata": metadata
    }

    # --- Send request to Paystack ---
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }


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