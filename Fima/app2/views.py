from django.shortcuts import render
from app1.models import CurrentTransaction,UserProfileInfo,TransactionHistory,Friends
from app1.views import add_notification,notification_count
from collections import defaultdict
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from datetime import date
# Create your views here.

passed_email = ""


def history(request):
    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user
    his_record = TransactionHistory.objects.order_by('date')
    
    dict_to_pass = {'his_record':his_record , 'curr_user':curr_user_email}
    return render(request,'app2/history.html',dict_to_pass)    


def find_required_email(email):
    required_user  = User.objects.filter(email = email)[0]
    return required_user

def settle_trans(request):
    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user
    curr_trans = CurrentTransaction.objects.order_by('tdate')
    his_trans = TransactionHistory.objects.order_by('date')


    if request.method == 'POST':
        search_id = request.POST.get('friend_id')
        passed_email = search_id
        print(passed_email)
        # pass all transactions from CurrentTransaction to TransactionHistory for that specific user
        # print(len(curr_trans))
        for trans in curr_trans:
            # print(trans)
            if str(trans.user_id1) == curr_user_email:
                if str(trans.user_id2) == passed_email:
                    his = TransactionHistory.objects.get_or_create(user_id1 = trans.user_id1 , user_id2 = trans.user_id2 ,
                    date= trans.tdate , Amount = trans.amount , lent = trans.lent , borrowed = trans.lent , 
                    Desc = trans.desc)[0]
                    his.save()
                    # print(trans.desc)
                    req_email = find_required_email(passed_email)
                    CurrentTransaction.objects.filter( user_id1 = request.user , user_id2 = req_email  ).delete()

            if str(trans.user_id1) == passed_email:
                if str(trans.user_id2) == curr_user_email:
                    his = TransactionHistory.objects.get_or_create(user_id1 = trans.user_id1 , user_id2 = trans.user_id2,
                    date= trans.tdate , Amount = trans.amount , lent = trans.lent , borrowed = trans.lent , 
                    Desc = trans.desc)[0]  
                    his.save()
                    req_email = find_required_email(passed_email)
                    CurrentTransaction.objects.filter( user_id1 = req_email , user_id2 =  request.user  ).delete()
    # adding notifications
    message1 = curr_user_email + " has settled all expenses on " + str(date.today())
    message2 = "you have settled tranctions with " + passed_email + " on " + str(date.today())
    required_e = User.objects.filter(email = passed_email)[0]

    add_notification(request.user,message2)
    add_notification(required_e,message1)

    return render(request,'app2/all_trans.html')    




def all_trans(request):

    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user
    trans_record = CurrentTransaction.objects.order_by('tdate')

     # FOR POST METHOD
    if request.method == 'POST':
        search_id = request.POST.get('friend_id')
        passed_email = search_id

        trans_record = {'trans_record':trans_record , 'curr_user':curr_user_email,'required_email':passed_email,'combined_email':[curr_user_email,passed_email]}
        return render(request,'app2/all_trans.html',trans_record)    
    else:
        return render(request,'app2/all_trans.html')    



    # current_user = request.user
    # curr_user_email = str( current_user.get_username() ) #got current user
    # trans_record = CurrentTransaction.objects.order_by('tdate')
    # print("somehitn")
    # print(passed_email)
    # trans_record = {'trans_record':trans_record , 'curr_user':curr_user_email,'required_email':passed_email}
    # return render(request,'app2/all_trans',trans_record)    
    



def home(request):  
    print("notification count="+notification_count(request.user))
    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user
    all_details = {'pos':0 ,'neg':0  ,'total':0 ,'pos_ratio':0 ,'nag_ratio':0}
    # two final dict for passing to template
    friends_amount = defaultdict(lambda: 0)
    friends_name = defaultdict(lambda: 'none') 

    # queried database
    trans_record = CurrentTransaction.objects.order_by('tdate')
    user_record = UserProfileInfo.objects.order_by('name')
    friends = Friends.objects.all()

    # storing record of all friends
    for f in friends:
        if str(f.user_id1) == curr_user_email:
            friends_name[str(f.user_id2)] = 'none'
            friends_amount[str(f.user_id2)] = 0
        elif str(f.user_id2) == curr_user_email:
            friends_name[str(f.user_id1)] = 'none'
            friends_amount[str(f.user_id1)] = 0


    all_user = list(user_record)
    all_trans = list(trans_record)

    # CODE TO CALCULATE NET AMOUNT
    for record in trans_record:
        if str(record.user_id1) == curr_user_email:
            friends_amount[ str(record.user_id2) ] += int(record.amount)
            all_details['pos'] +=  int(record.amount)
            # print(str(record.user_id2)+'test1')

        elif str(record.user_id2) == curr_user_email:
            # print(str(record.user_id1)+'test2')
            friends_amount[ str(record.user_id1) ] -= int(record.amount)
            all_details['neg'] +=  int(record.amount)
    all_details['total'] = abs(all_details['pos'] - all_details['neg'])
    #percent of distribution
    try:
        all_details['pos_ratio'] =  int( all_details['pos'] / ( all_details['pos'] + all_details['neg']) ) *100
        all_details['neg_ratio'] =  int( all_details['neg'] / ( all_details['pos'] + all_details['neg']) ) *100
    except:
        None
    # DISPLAY USERNAME ISTEAD OF EMAIL
    for users in all_user:
        if friends_name[ str(users.user) ] == 'none'  :
            friends_name[ str(users.user) ] = users.name

    try:
        friends_name.pop(curr_user_email) # idk how current user was also getting added to the dict
        friends_name.pop(curr_user_email)
        friends_amount.pop(curr_user_email)
    except:
        None
    # for key,_ in friends_name.items():
    #     print(friends_name[key],friends_amount[key])
    
    # friends_name and friends_amount are two dict having email as key and name and amount as value 
    trans_dict = {'names': friends_name,'amount':friends_amount, 'TITLE':'HOME','curr_user':current_user.get_username() , 'all_details': all_details}

    # my_dict = {'insert_content':"hello I am from first app"}
    return render(request, 'app2/home.html',trans_dict)