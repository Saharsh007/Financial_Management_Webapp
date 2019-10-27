from django import template
from app1.views import notification_count

register = template.Library()
@register.filter(name='get_no_of_notifications')

def get_no_of_notifications(string_no_use,curr_user):
    """
    This returns the value of a dict given its key
    """ 
    count = notification_count(curr_user)
    return count


