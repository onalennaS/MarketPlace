from django.shortcuts import render, redirect
from functools import wraps


def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect to login page if not authenticated
    return _wrapped_view


import re
from datetime import datetime

def validate_full_name(full_name):
    return bool(full_name.strip()) and len(full_name) >= 3

def validate_dob(dob):
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = (today - birth_date).days // 365
        return age >= 16  # Must be 16+ years old
    except ValueError:
        return False

def validate_phone(phone):
    pattern = r"^(\+27|0)[6-8][0-9]{8}$"
    return re.match(pattern, phone) is not None

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def validate_address(address):
    return bool(address.strip())

def validate_file_uploaded(file):
    return file is not None

def validate_sa_id(id_number):
    """
    Validate South African ID:
    - 13 digits
    - Luhn algorithm check
    """
    if not id_number.isdigit() or len(id_number) != 13:
        return False

    # Luhn algorithm for checksum
    def luhn_checksum(id_num):
        digits = [int(d) for d in id_num]
        odd_sum = sum(digits[-1::-2])
        even_sum = sum(sum(divmod(2 * d, 10)) for d in digits[-2::-2])
        return (odd_sum + even_sum) % 10 == 0

    return luhn_checksum(id_number)

def validate_transport(transport):
    valid_options = ['Skateboard', 'Bicycle', 'Hoverboard', 'Roller Blades', 'Car', 'Motorcycle', 'Walking']
    return transport.capitalize() in valid_options

def validate_agreements(terms, privacy, conduct):
    return terms and privacy and conduct
