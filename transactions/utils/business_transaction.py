from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..models import BusinessWallet, BusinessTransaction
from decimal import Decimal
from user.wrap_models.cart_models import Cart, CartExtra, Wishlist,CartAddons,CartDeliveryMethod,CartDeliveryAddress
from seller.wrap_models.orders_model import Order, OrderItem, OrderExtra, OrderAddons,OrderAddress
from seller.wrap_models.product_model import Product, Extras,Addon
def transfer_money_to_business(user,business,order,ref):
    sender = user
    receiver = business
    order = order.order_id
    transaction_type = "Purchase"


    transaction = BusinessTransaction.objects.filter(ref=ref).first()
    if transaction:
        transaction.sender = sender
        transaction.receiver = receiver
        transaction.transaction_type = transaction_type
        transaction.status = "success"
        transaction.save()
        return transaction.id

    receiver_wallet = BusinessWallet.objects.filter(business=receiver).first()
    if not receiver_wallet:
    	receiver_wallet = BusinessWallet.objects.create(business=receiver)
    	receiver_wallet.save()

    
    receiver_wallet.balance = Decimal(str(receiver_wallet.balance))  + Decimal(str(transaction.amount))
    receiver_wallet.total = Decimal(str(receiver_wallet.total)) + Decimal(str(transaction.amount))
    receiver_wallet.save()
    return False


def create_transaction(ref,amount,fees):
    transaction = BusinessTransaction.objects.create(ref=ref, fees=fees, amount=amount)
    transaction.save()
    return True

def withdraw_business_funds(business,amount):
   
    receiver = business
    amount = amount
    transaction_type = "Withdrawal"

    receiver_wallet = BusinessWallet.objects.filter(business=receiver).first()

    if receiver_wallet.balance < amount :
    	return None

     # Prevents race conditions

    receiver_wallet.balance -= Decimal(amount)
    receiver_wallet.save()

    transaction = BusinessTransaction.objects.create(sender=receiver.owner, receiver=receiver, amount=amount, status="Success", transaction_type=transaction_type)
    transaction.save()
    return True

def clean_cart(user,ref,order):
    transaction = BusinessTransaction.objects.filter(ref=order.ref).first()
    order.total_amount = transaction.total_amount
    order.save()
    cart_items = Cart.objects.filter(user=user).all()
    cart_extras = CartExtra.objects.filter(user=user).all()
    delivery_method = CartDeliveryMethod.objects.filter(user=user).first()
    address = CartDeliveryAddress.objects.filter(user=user).first()
    for item in cart_items:
        order_item = OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity)
        order_item.save()
        cart_addons = CartAddons.objects.filter(cart=item).all()
        if cart_addons:
            for addon in cart_addons:
                order_addon = OrderAddons.objects.create(product=order_item, addon=addon.addon)
                order_addon.save()
        product_to_update = Product.objects.filter(id=item.product.id).first()
        if product_to_update:
            product_to_update.quantity -= 1
            product_to_update.save()
        item.delete()
    if cart_extras:
        for extra in cart_extras:
            order_extra = OrderExtra.objects.create(order=order,extra=extra.extra,quantity=extra.quantity)
            order_extra.save()
            extra.delete()
    if delivery_method.method == "delivery":
        if address.address_type == "residential":
            order_address = OrderAddress.objects.create(order=order,address_line_1=address.house_no, address_line_2=address.street,address_line_3=address.complex_name,address_line_4=address.area,notes=address.notes)
            order_address.save()
        elif address.address_type == "campus":
            order_address = OrderAddress.objects.create(order=order,address_line_1=address.instutition, address_line_2=address.block,address_line_3=address.venue,notes=address.notes)
            order_address.save()
    return True