from django.shortcuts import render
from app1.models import CurrentTransaction,UserProfileInfo,TransactionHistory
from collections import defaultdict
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

passed_email = ""


def history(request):
    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user
    his_record = TransactionHistory.object.order_by('date')
    
    dict_to_pass = {'his_record':his_record , 'curr_user':curr_user_email}
    return render(request,'app2/histroy.html',dict_to_pass)    



def settle_trans(request):
    current_user = request.user
    curr_user_email = str( current_user.get_username() ) #got current user
    curr_trans = CurrentTransaction.objects.order_by('tdate')
    his_trans = TransactionHistory.objects.order_by('date')


    if request.method == 'POST':
        search_id = request.POST.get('friend_id')
        passed_email = search_id
        # pass all transactions from CurrentTransaction to TransactionHistory for that specific user
        for trans in curr_trans:
            if str(trans.user_id1) == curr_user_email:
                if str(trans.user_id2) == passed_email:
                    his = TransactionHistory.objects.get_or_create(user_id1 = trans.user_id1 , user_id2 = trans.user_id2 ,
                    date= trans.tdate , Amount = trans.amount , lent = trans.lent , borrowed = trans.lent , 
                    Desc = trans.desc)[0]
                    his.save()
                    CurrentTransaction.objects.filter(user_id1 = curr_user_email , user_id2 = passed_email).delete()

            if str(trans.user_id1) == passed_email:
                if str(trans.user_id2) == curr_user_email:
                    his = TransactionHistory.objects.get_or_create(user_id1 = trans.user_id1 , user_id2 = trans.user_id2,
                    date= trans.tdate , Amount = trans.amount , lent = trans.lent , borrowed = trans.lent , 
                    Desc = trans.desc)[0]  
                    his.save()
                    CurrentTransaction.objects.filter(user_id1 = passed_email , user_id2 = curr_user_email).delete()




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