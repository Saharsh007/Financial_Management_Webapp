from django.shortcuts import render
from app1.forms import UserForm,UserProfileInfoForm,UpdateProfileForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app1.models import CurrentTransaction,Friends,UserProfileInfo,OldNotification,NewNotification
from django.contrib.auth.models import User

from app1.forms import TransactionForm
from django.utils import timezone
from django.contrib.auth.hashers import check_password
import copy
from datetime import date
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages

# Create your views here.

is_delete_message=False
is_update_message=False

@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
	if(is_update_message):
		messages.add_message(request, messages.INFO, 'Account Details Updated SuccesFully, Login Again')
	
	elif(is_delete_message):
		messages.add_message(request, messages.INFO, 'Account Deleted SuccesFully, Good Bye!')

	else:
		messages.add_message(request, messages.INFO, 'You Have Logged Out SuccesFully, Good Bye!')


def index(request):
	return render(request,'app1/index.html')

@login_required
def special(request):
	return HttpResponse("You Are logged in !")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def register(request):
	registered=False
	error_s = ""
	if(request.method=='POST'):
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileInfoForm(data=request.POST)

		if(user_form.is_valid() and profile_form.is_valid()):
			user=user_form.save(commit=False)
			user.set_password(user.password)
			user.username=user.email
			user.save()
			profile=profile_form.save(commit=False)
			profile.user=user

			# Check if they provided a profile picture
			if 'profile_pic' in request.FILES:
				print('found it')
				# If yes, then grab it from the POST form reply
				profile.profile_pic = request.FILES['profile_pic']

			# Now save model
			profile.save()
			registered=True

		else:
			print(user_form.errors,profile_form.errors)
			error_s1=	str(user_form.errors)
			error_s2 = str(profile_form.errors)
			user_form=UserForm()
			return render(request,'app1/registration.html',{'error_s1':error_s1,'error_s2':error_s2,'user_form':user_form,
						   'profile_form':profile_form})
			
	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
	return render(request,'app1/registration.html',
						  {'user_form':user_form,
						   'profile_form':profile_form,
						   'registered':registered})

def user_login(request):
	global is_check_notofication
	global is_delete_message
	global is_update_message
	is_check_notofication=False
	is_delete_message=False
	is_update_message=False
	if(request.method=="POST"):
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if(user):
			if(user.is_active):
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account was inactive.")

		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return render(request, 'app1/login.html', {'failed_login':True})
	else:
		return render(request, 'app1/login.html', {})

add_friend=None
@login_required
def user_search(request):
	global add_friend
	if(request.method=='POST'):
		print("I am in if 1")
		query=request.POST.get('q')
		# print(query)
		cur_user=request.user
		# print(request.POST.get('add'),add_friend)
		if(request.POST.get('add') and add_friend):
			f1=Friends()
			f1.user_id1=User.objects.get(id=request.user.id)
			f1.user_id2=User.objects.get(id=add_friend.id)
			f1.save()
			f2=Friends()
			f2.user_id2=User.objects.get(id=request.user.id)
			f2.user_id1=User.objects.get(id=add_friend.id)
			f2.save()
			message1 =request.user.email+" has added you as friend on "+str(date.today())
			message_curr="You Have added " + add_friend.email + " as your friend on " + str(date.today())
			add_notification(add_friend,message1)
			add_notification(request.user,message_curr)
			return render(request, 'app1/search.html',{'success':True} )
		elif(query is not None):
			is_exist=False
			result=User.objects.filter(email=query)
			if(result.exists() and result[0].username!=request.user.username):
				# print(request.user.username)
				is_friend=False
				is_friend_query=Friends.objects.filter(user_id1=request.user.id,
					user_id2=result[0].id)
				if(is_friend_query.exists()):
					is_friend=True
				else:
					add_friend=result[0]
				return render(request,'app1/search.html',{'result':result[0],'is_friend':is_friend})
			else:
				return render(request,'app1/search.html')

		else:
			return render(request,'app1/search.html')
	else:
		print("I am in else 1")
		return render(request,'app1/search.html')




passed_email=None
@login_required
def make_transaction(request):
	global passed_email
	if(request.method=='POST'):
		print(request.POST)
		if('show' in request.POST):
			form=TransactionForm()
			passed_email = request.POST.get('friend_id')
			print("Show"+passed_email)
			return render(request,'app1/transaction.html',{"passed_email":passed_email,'form':form})

		else:
			print("Add"+passed_email)
			form=TransactionForm(request.POST)
			is_click=True
			to_user=User.objects.filter(email=passed_email)
			if(form.is_valid()):
				print("Validation Success")
				action=form.cleaned_data['Action']
				amount=form.cleaned_data['Amount']
				desc=form.cleaned_data['Desc']
				if(to_user.exists()):
					to_friend=Friends.objects.filter(user_id1=request.user.id,
							user_id2=to_user[0].id)
					if(to_friend.exists()):
						new_transaction=CurrentTransaction()
						print("action="+str(action))
						print(UserProfileInfo.objects.filter(user_id=
								to_friend[0].user_id2.id))
						if(action=='Lent'):
							new_transaction.user_id1=request.user
							new_transaction.user_id2=User.objects.get(id=to_friend[0].user_id2.id)
							new_transaction.lent=UserProfileInfo.objects.filter(user=
								request.user)[0].name
							new_transaction.borrowed=UserProfileInfo.objects.filter(user=
								to_friend[0].user_id2)[0].name
							
							message_curr ="You Have Lent Rs "+str(amount)+" to "+to_friend[0].user_id2.email+" on "+str(date.today())
							message1="You Have Borrowed Rs "+str(amount)+" from "+request.user.email +" on "+str(date.today())
							add_notification(to_friend[0].user_id2,message1)
							add_notification(request.user,message_curr)
							
						else:
							new_transaction.user_id2=request.user
							new_transaction.user_id1=User.objects.get(id=to_friend[0].user_id2.id)
							new_transaction.borrowed=UserProfileInfo.objects.filter(user=
								request.user)[0].name
							new_transaction.lent=UserProfileInfo.objects.filter(user=
								to_friend[0].user_id2)[0].name

							message1 ="You Have Lent Rs"+str(amount)+" to "+request.user.email+" on "+str(date.today())
							message_curr="You Have Borrowed Rs"+str(amount)+" from "+to_friend[0].user_id2.email+" on "+str(date.today())
							add_notification(to_friend[0].user_id2,message1)
							add_notification(request.user,message_curr)

						new_transaction.amount=amount
						new_transaction.desc=desc
						new_transaction.tdate=timezone.now()
						new_transaction.save()
						return render(request,'app1/transaction.html',{'to_friend':to_friend,'form':form,
						"passed_email":passed_email})

					else:
						return render(request,'app1/transaction.html',{'to_user':to_user,'form':form,
						"passed_email":passed_email}) 

				else:
					print("Validation Failed")
					return HttpResponse("invalid Form")

			else:
				return render(request,'app1/transaction.html',{'form':form,"passed_email":passed_email})

	else:
		form=TransactionForm()
		return render(request,'app1/transaction.html',{'form':form,"passed_email":passed_email})





@login_required
def user_profile_view(request):
	user_info=UserProfileInfo.objects.filter(user=request.user)[0]
	return render(request,"app1/show_profile.html",{"user":request.user,"user_info":user_info})







@login_required
def user_profile(request):
	global is_update_message
	if(request.method=='POST'):
		form=UpdateProfileForm(request.POST)
		is_clicked=True
		if(form.is_valid()):
			print("form is valid")
			new_name=form.cleaned_data['name']
			new_phone_number=form.cleaned_data['phone']
			new_user_address=form.cleaned_data['address']
			old_password=form.cleaned_data['old_password']
		
			if(check_password(old_password,request.user.password)):
				print("Check Password Success")
				new_password=form.cleaned_data['new_password']
				conf_password=form.cleaned_data['conf_password']
				is_update=False
				if(new_password==conf_password):
					is_update=True
					new_user=request.user
					new_user_profile=UserProfileInfo.objects.filter(user=request.user)[0]
					new_user.set_password(new_password)
					new_user_profile.name=new_name
					new_user_profile.phone_number=new_phone_number
					new_user_profile.user_address=new_user_address
					new_user.save()
					new_user_profile.save()
					is_update_message=True
					return user_logout(request)
				print(is_update)
				return render(request,'app1/profile.html',{'is_update':is_update,'form':form})

			return render(request,'app1/profile.html',{'is_clicked':is_clicked,'form':form})
		
		else:
			ValidationError(_('Invalid value'), code='invalid')
	else:
		form=UpdateProfileForm(initial={'name': UserProfileInfo.objects.filter(user=request.user)[0].name,
		'phone':UserProfileInfo.objects.filter(user=request.user)[0].phone_number,
		'address':UserProfileInfo.objects.filter(user=request.user)[0].user_address})
		return render(request,'app1/profile.html',{'form':form})




@login_required
def show_notification(request):
	old_not=list(OldNotification.objects.filter(user_id=request.user)) 
	old_not = reversed(old_not)
	new_not=list(NewNotification.objects.filter(user_id=request.user))
	move_notification(request.user)
	return render(request,'app1/notification.html',{'old_not':old_not,'new_not':new_not})



@login_required
def delete_account(request):
	global is_delete_message
	if(request.method=='POST'):
		can=False
		curr_t1=CurrentTransaction.objects.filter(user_id1=request.user)
		curr_t2=CurrentTransaction.objects.filter(user_id2=request.user)
		print(curr_t1)
		print(curr_t2)
		if(curr_t1.exists() or curr_t2.exists()):
			return render(request,'app1/delete.html',{"can":can})
		else:
			can=True
			u=User.objects.get(username=request.user.username)
			is_delete_message=True
			message1="You Friend "+ str(u.email) +" has left FIMA after settling all the expenses " +" on "+str(date.today())
			all_friends=list(Friends.objects.all())
			for friends in all_friends:
				if(friends.user_id1==u):
					add_notification(friends.user_id2,message1)
			u.delete()
			return user_logout(request)
	else:
		return render(request,'app1/delete.html')







def notification_count(user):
	return str(NewNotification.objects.filter(user_id=user).count())

def add_notification(user,message):
	new_notification=NewNotification()
	new_notification.user_id=user
	new_notification.desc=message
	new_notification.save()

def move_notification(user):
	all_obj=NewNotification.objects.filter(user_id=user)
	for obj in all_obj:
		old_obj=OldNotification()
		old_obj.user_id=obj.user_id	
		old_obj.desc=obj.desc
		old_obj.date=obj.date
		old_obj.save()
	NewNotification.objects.filter(user_id=user).delete()



