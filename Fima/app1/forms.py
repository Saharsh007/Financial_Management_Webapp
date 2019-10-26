
from django import forms
from app1.models import UserProfileInfo
from django.contrib.auth.models import User
from app1.models import CurrentTransaction

class UserForm(forms.ModelForm):
	class Meta():
		model=User
		fields=('email','password')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('name','gender','dob')

class TransactionForm(forms.Form):
	Email=forms.EmailField(label='Email',max_length=50)
	Amount=forms.IntegerField(label='Amount')
	Action=forms.ChoiceField(choices=[('Lent','Lent'),('Borrowed','Borrowed')])
	Desc=forms.CharField(label='Description',max_length=20)

class UpdateProfileForm(forms.Form):
	name=forms.CharField(label='New Name',max_length=50)
	old_password=forms.CharField(label='Old password',widget=forms.PasswordInput)
	new_password=forms.CharField(label='New password',widget=forms.PasswordInput)
	conf_password=forms.CharField(label='Confirm password',widget=forms.PasswordInput)
