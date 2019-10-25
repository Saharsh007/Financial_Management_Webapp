from django import template

register = template.Library()
@register.filter(name='value_of_key')

def value_of_key(dictionary,key):
    """
    This returns the value of a dict given its key
    """
    return dictionary[key]

@register.filter(name='check_pos')

def check_pos(dictionary,key):
    """
    This returns the 1 if value is poistive else 0
    """
    if dictionary[key] > 0:
        return 1
    else:
        return 0


@register.filter(name='return_pos')

def return_pos(dictionary,key):
    """
    This returns positive value
    """

    return abs(dictionary[key])
