import re

def is_valid_string(value, min_length=1, max_length=255):
    """Check if the value is a valid non-empty string with a specified length."""
    return isinstance(value, str) and min_length <= len(value) <= max_length

def is_valid_email(email):
    """Validate email format using regex."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_regex, email)) if email else False

def is_valid_phone_number(phone):
    """Validate phone number (accepts digits and optional + at start)."""
    phone_regex = r"^\+?[0-9]{7,15}$"
    return bool(re.match(phone_regex, phone)) if phone else False

def is_valid_postal_code(postal_code):
    """Validate postal code (numbers only, typically 4-10 digits)."""
    postal_code_regex = r"^\d{4,10}$"
    return bool(re.match(postal_code_regex, postal_code)) if postal_code else False

def validate_registration_number(reg_number):
    """Ensure registration number is alphanumeric and has a valid length."""
    return bool(re.match(r"^[A-Za-z0-9\-]+$", reg_number)) if reg_number else False

def validate_business_data(data):
    """Validate all fields in the business registration request."""
    errors = {}

    # Required fields validation
    required_fields = [
        "name", "business_type", "description", "registration_number",
        "category", "phone", "email", "address_line_1", "city",
        "province", "postal_code", "address_type"
    ]

    for field in required_fields:
        if not data.get(field) or not is_valid_string(data.get(field)):
            errors[field] = f"{field.replace('_', ' ').title()} is required and must be a valid string."

    # Specific field validation
    if data.get("email") and not is_valid_email(data["email"]):
        errors["email"] = "Invalid email format."

    if data.get("phone") and not is_valid_phone_number(data["phone"]):
        errors["phone"] = "Invalid phone number format. Must be 7-15 digits."

    if data.get("telephone") and not is_valid_phone_number(data["telephone"]):
        errors["telephone"] = "Invalid telephone number format."

    if data.get("postal_code") and not is_valid_postal_code(data["postal_code"]):
        errors["postal_code"] = "Invalid postal code format."

    if data.get("registration_number") and not validate_registration_number(data["registration_number"]):
        errors["registration_number"] = "Invalid registration number format."

    return errors if errors else None
