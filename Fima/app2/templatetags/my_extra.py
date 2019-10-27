from django import template
from app1.views import notification_count

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
    if dictionary[key] >= 0:
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



@register.filter(name='check_for_history_of_transaction')

def check_for_history_of_transaction(trans,curr_user):
    """
    This returns if the  transactions which has user1 as curr_user
    """
    if str(trans.user_id1) == curr_user:
            return True
    elif str(trans.user_id2) == curr_user:
            return True
    else:
        return False



@register.filter(name='get_number_of__new_notifications')

def get_number_of__new_notifications(a_string):
    """
    This returns total number of new notifications
    """
    current_user = user
    curr_user_email = str( current_user.get_username() ) #got current user



@register.filter(name='checksize')

def checksize(a_dict):
    """
    checks if size of dict is zero
    """
    for key,value in a_dict.items():
        print(key,value)
    if len(a_dict)  > 0:
        return True
    else:
        return False

@register.filter(name='check_object_size')

def check_object_size(object,curr_user):
    """
    checks if size of dict is zero
    """
    print(len(object))
    Flag = False
    for t in object:
        if check_for_history_of_transaction(t,curr_user) :
            Flag = True 
    if Flag == True:
        return True
    else:
        return False



@register.filter(name='get_no_of_notifications')

def get_no_of_notifications(string_no_use,curr_user):
    """
    This returns the value of a dict given its key
    """ 
    count = notification_count(curr_user)
    return count