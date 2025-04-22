import requests
from django.conf import settings
from .business_transaction import create_transaction
#get order 
#get number of items in the order 
#calculate the product fee on each order in this case its R4 per item
#get the total prodcut fee
#minus the paystack fee from the product fee
#that remainng product fee is plartform cut
def get_discount(cart_items):
    discount_factor = sum(item.quantity for item in cart_items)
    discount = 4

    if discount_factor < 3:
        return 0
    elif discount_factor == 3:
        return discount * 1
    else:
        # Calculate how many 2-step intervals after 3
        n = (discount_factor - 4) // 2 + 1
        return discount * (n + 0.5)


def initiate_split_payment(email, total_amount, seller_subaccount, delivery_amount, order, cart_items,cart_extras):
    discount= get_discount(cart_items)
    total_amount = float(total_amount) - discount
    delivery_amount = float(delivery_amount)
    items_count = 0
    extras_count = 0
    for item in cart_items:
        items_count += item.quantity

    if items_count == 0:
        items_count = 1

    for extra in cart_extras:
        extras_count += 1


    product_fee = (4 * items_count) - discount#- ((4*items_count)*25/100)
    extra_fee = (0.55 * extras_count)
    extra_fee_kobo = extra_fee * 100
    #product_fee_kobo = float(product_fee * 100)

    paystack_fee = (total_amount * (2.9/100)) + 1 
    paystack_fee_vat = paystack_fee * 1.15
    product_fee_minus_paystack_fee_vat = product_fee - paystack_fee_vat
    if product_fee_minus_paystack_fee_vat > 1 :
        platform_cut = (product_fee_minus_paystack_fee_vat*(30/100) ) + paystack_fee_vat 
    
    else:
        platform_cut = product_fee_minus_paystack_fee_vat + paystack_fee_vat 

    platform_cut_kobo = platform_cut  * 100
    # --- Breakdown in rands ---
    product_total = (total_amount - delivery_amount) 
    product_total_kobo = float(product_total * 100)
    delivery_kobo = float((delivery_amount) * 100)
    grand_total_kobo = float(total_amount * 100)

    # --- Fixed platform cut ---
    #platform_cut_kobo = (items_count * 0.60 )* 100# R0.60 in kobo

    # Ensure we don’t assign more than available product value
    if product_total_kobo <= platform_cut_kobo:
        platform_cut_kobo = 0  # fallback, no split if value is too small

    seller_cut_kobo = product_total_kobo  - platform_cut_kobo - extra_fee_kobo

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
        transaction = create_transaction(data['reference'],seller_cut_kobo/100,platform_cut )
        return {
            "authorization_url": data["authorization_url"]
        }
    else:
        #order.delete()
        print("Payment error:", response.json())
        return None