from ..wrap_models.business_model import BusinessInformation

def validate_business_data(data):
    required_fields = ['business_id', 'name', 'category', 'price', 'quantity', 'description']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"

    try:
        price = float(data['price'])
        if price < 0:
            return "Price must be a positive number."
    except ValueError:
        return "Invalid price format. Must be a number."

    try:
        quantity = int(data['quantity'])
        if quantity < 0:
            return "Quantity must be a positive integer."
    except ValueError:
        return "Invalid quantity format. Must be an integer."

    if not BusinessInformation.objects.filter(id=data['business_id']).exists():
        return "Invalid business_id. Business not found."

    return None  # No errors
