from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..models import BusinessWallet, BusinessTransaction
from decimal import Decimal

def transfer_money_to_business(user,business,amount,order):
    sender = user
    receiver = business
    amount = amount
    order = order.order_id
    transaction_type = "Purchase"

    receiver_wallet = BusinessWallet.objects.filter(business=receiver).first()
    if not receiver_wallet:
    	receiver_wallet = BusinessWallet.objects.create(business=receiver)
    	receiver_wallet.save()

    
    receiver_wallet.balance += amount
    receiver_wallet.total += amount
    receiver_wallet.save()

    transaction = BusinessTransaction.objects.create(sender=sender, receiver=receiver, amount=amount,ref=order, status="Success", transaction_type=transaction_type)
    transaction.save()
    return transaction.id

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