
from django import forms
from app1.models import UserProfileInfo
from django.contrib.auth.models import User
from app1.models import CurrentTransaction

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model=User
		fields=('email','password')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('name','gender','dob','profile_pic')

class TransactionForm(forms.Form):
	Amount=forms.IntegerField(label='Amount',widget=forms.NumberInput(attrs={'id':'Amount','class':'text_field'}))
	Action=forms.ChoiceField(choices=[('Lent','Lent'),('Borrowed','Borrowed')])
	Desc=forms.CharField(label='Description',max_length=20,widget=forms.TextInput(attrs={'id':'Desc','class':'text_field'}))

class UpdateProfileForm(forms.Form):
	name = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={'id':'name','class':'text_field'}) )
	old_password = forms.CharField(label='Old password',widget=forms.PasswordInput(attrs={'id':'old_password','class':'text_field'}) )
	new_password = forms.CharField(label='New password',widget=forms.PasswordInput(attrs={'id':'new_password','class':'text_field'}) )
	conf_password = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'id':'conf_password','class':'text_field'}) )