# onlineschoolapp/templatetags/quiz_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), "-")

@register.filter
def first_correct(choices):
    for choice in choices:
        if choice.is_correct:
            return choice
    return None

@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)