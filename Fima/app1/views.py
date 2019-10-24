from django.shortcuts import render
from app1.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app1.models import CurrentTransaction,Friends
from django.contrib.auth.models import User
# Create your views here.

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
			profile.save()
			regitered=True

		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
	return render(request,'app1/registration.html',
						  {'user_form':user_form,
						   'profile_form':profile_form,
						   'registered':registered})

def user_login(request):
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
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'app1/login.html', {})

@login_required
def user_search(request):
	if(request.method=='POST'):
		print("I am in if 1")
		query=request.POST['q']
		print(query)
		cur_user=request.user
		if(query is not None):
			is_exist=False
			result=User.objects.filter(email=query)
			if(result.exists() and result[0].username!=request.user.username):
				print(request.user.username)
				is_friend=False;
				is_friend_query=Friends.objects.filter(user_id1=request.user.id,
					user_id2=result[0].id)
				if(is_friend_query.exists()):
					is_friend=True
				return render(request,'app1/search.html',{'result':result[0],'is_friend':is_friend})
			else:
				return render(request,'app1/search.html')

		else:
			return render(request,'app1/search.html')

	else:
		print("I am in else 1")
		return render(request,'app1/search.html')