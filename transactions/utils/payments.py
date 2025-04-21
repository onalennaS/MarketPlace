import requests
from django.conf import settings
#get order 
#get number of items in the order 
#calculate the product fee on each order in this case its R4 per item
#get the total prodcut fee
#minus the paystack fee from the product fee
#that remainng product fee is plartform cut

def initiate_split_payment(email, total_amount, seller_subaccount, delivery_amount, order, cart_items):
    total_amount = float(total_amount)
    delivery_amount = float(delivery_amount)
    items_count = 0
    for item in cart_items:
        items_count += 1

    if items_count == 0:
        items_count = 1
        
    product_fee = 4 * items_count
    product_fee_kobo = int(product_fee * 100)

    # paystack_fee = (total_amount * (2.9/100)) + 1 
    # paystack_fee_vat = paystack_fee * 1.15
    # product_fee_minus_paystack_fee_vat = product_fee - paystack_fee_vat


    # --- Breakdown in rands ---
    product_total = (total_amount - delivery_amount) 
    product_total_kobo = int(product_total * 100)
    delivery_kobo = int((delivery_amount) * 100)
    grand_total_kobo = int(total_amount * 100)

    # --- Fixed platform cut ---
    platform_cut_kobo = 60  # R0.60 in kobo

    # Ensure we don’t assign more than available product value
    if product_total_kobo <= platform_cut_kobo:
        platform_cut_kobo = 0  # fallback, no split if value is too small

    seller_cut_kobo = product_total_kobo  - platform_cut_kobo - product_fee_kobo
 

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
        #order.delete()
        print("Payment error:", response.json())
        return None