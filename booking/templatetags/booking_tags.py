from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply a value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def currency_inr(value):
    """Format value as INR currency."""
    try:
        return f"₹{float(value):,.0f}"
    except (ValueError, TypeError):
        return value
