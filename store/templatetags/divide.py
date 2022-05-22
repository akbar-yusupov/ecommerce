from django import template

register = template.Library()


@register.simple_tag
def divide_partition(value, arg):
    try:
        return int(value) // int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.simple_tag
def divide_remainder(value, arg):
    try:
        a = int(value) / int(arg)
        a = a - int(a)
        if a >= 0.5:
            return "Yes"
        else:
            return "No"
    except (ValueError, ZeroDivisionError):
        return None
