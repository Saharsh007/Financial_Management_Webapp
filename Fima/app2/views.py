from django.shortcuts import render
from app1.models import CurrentTransaction,UserProfileInfo
from collections import defaultdict
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

passed_email = ""

def all_trans(request):
    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user
    trans_record = CurrentTransaction.objects.order_by('tdate')
    # print(search_id)

     # FOR POST METHOD
    if request.method == 'POST':
        search_id = request.POST.get('friend_id')
        passed_email = search_id

        print(passed_email)
        # print("somehitn")
        # print(passed_email)

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
   
    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user

    # two final dict for passing to template
    friends_amount = defaultdict(lambda: 0)
    friends_name = defaultdict(lambda: 'none') 

    # queried database
    trans_record = CurrentTransaction.objects.order_by('tdate')
    user_record = UserProfileInfo.objects.order_by('name')
    all_user = list(user_record)
    all_trans = list(trans_record)

    # CODE TO CALCULATE NET AMOUNT
    for record in trans_record:
        if str(record.user_id1) == curr_user_email:
            friends_amount[ str(record.user_id2) ] += int(record.amount)
            # print(str(record.user_id2)+'test1')

        elif str(record.user_id2) == curr_user_email:
            # print(str(record.user_id1)+'test2')
            friends_amount[ str(record.user_id1) ] -= int(record.amount)

    # DISPLAY USERNAME ISTEAD OF EMAIL
    for users in all_user:
        if friends_name[ str(users.user) ] == 'none':
            friends_name[ str(users.user) ] = users.name

    friends_name.pop(curr_user_email) # idk how current user was also getting added to the dict
    
    # for key,_ in friends_name.items():
    #     print(friends_name[key],friends_amount[key])
    
    # friends_name and friends_amount are two dict having email as key and name and amount as value 
    trans_dict = {'names': friends_name,'amount':friends_amount, 'TITLE':'HOME','curr_user':current_user.get_username()}

    # my_dict = {'insert_content':"hello I am from first app"}
    return render(request, 'app2/home.html',trans_dict)