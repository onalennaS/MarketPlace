from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..models import DeliveryWallet, DeliveryTransaction
from decimal import Decimal



def transfer_money_to_courier(user=None,amount=0.00,order_id=None):
   
    transaction_type = "Payment"
     
    if user:
        receiver_wallet = DeliveryWallet.objects.filter(user=user).first()
        if not receiver_wallet:
        	receiver_wallet = DeliveryWallet.objects.create(user=user)
        	receiver_wallet.save()

    
        receiver_wallet.balance = Decimal(str(receiver_wallet.balance))  + Decimal(str(amount))
        receiver_wallet.total = Decimal(str(receiver_wallet.total)) + Decimal(str(amount))
        receiver_wallet.save()
        transaction = DeliveryTransaction.objects.create(user=user,order_id=order_id, amount=amount, status="Success", transaction_type=transaction_type)
        transaction.save()
    return True

def withdraw_courier_funds(user,amount):
   
    receiver = user
    amount = Decimal(amount)
    transaction_type = "Withdrawal"

    receiver_wallet = DeliveryWallet.objects.filter(user=receiver).first()

    if receiver_wallet.balance < amount :
    	return None

     # Prevents race conditions

    receiver_wallet.balance -= amount
    receiver_wallet.save()

    transaction = DeliveryTransaction.objects.create(user=receiver,order_id=None, amount=amount, status="Pending", transaction_type=transaction_type)
    transaction.save()
    return transaction.ref