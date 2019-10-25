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


@register.filter(name='find_trans')

def find_trans(trans,curr_email):
    """
    This returns if the  transactions which has user1 as curr_user
    """
    if str(trans.user_id1) == curr_email:
        return True
    else:
        return False 


        



@register.filter(name='check_for_this_user_transaction')

def check_for_this_user_transaction(trans,emails):
    """
    This returns if the  transactions which has user1 as curr_user
    """
    if str(trans.user_id1) == emails[0]:
        if str(trans.user_id2) == emails[1]:
            return True
        else:
            return False
    elif str(trans.user_id1) == emails[1]:
        if str(trans.user_id2) == emails[0]:
            return True
        else:
            return False
    else:
        return False
