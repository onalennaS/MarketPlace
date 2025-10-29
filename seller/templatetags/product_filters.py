from django import template

register = template.Library()

@register.filter
def top_by(products, field):
    """Return the single product with the highest value for a given field."""
    try:
        return max(products, key=lambda p: getattr(p, field, 0))
    except Exception:
        return None
