
from django import forms
from app1.models import UserProfileInfo
from django.contrib.auth.models import User
from app1.models import CurrentTransaction

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model=User
		fields=('email','password')
		widgets = {
			'email': forms.TextInput(attrs={'id':'email','class': 'text_field'}),
			'password':forms.PasswordInput(attrs={'id':'password','class':'text_field'}),
			}

class UserProfileInfoForm(forms.ModelForm):
	 class Meta():
		 model = UserProfileInfo
		 fields = ('name','gender','dob','phone_number','user_address','profile_pic')
		 widgets = {
			'name': forms.TextInput(attrs={'id':'name','class': 'text_field'}),
			'phone_number': forms.TextInput(attrs={'id':'phone_number','class': 'text_field'}),
			'user_address': forms.TextInput(attrs={'id':'user_address','class': 'text_field'}),
			'dob': forms.TextInput(attrs={'id':'dob','class': 'text_field'}),
			
			}

class TransactionForm(forms.Form):
	Amount=forms.IntegerField(label='Amount',widget=forms.NumberInput(attrs={'id':'Amount','class':'text_field'}))
	Action=forms.ChoiceField(choices=[('Lent','Lent'),('Borrowed','Borrowed')])
	Desc=forms.CharField(label='Description',max_length=20,widget=forms.TextInput(attrs={'id':'Desc','class':'text_field'}))

class UpdateProfileForm(forms.Form):
	name = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={'id':'name','class':'text_field'}) )
	phone = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={'id':'phone','class':'text_field'}) )
	address = forms.CharField(max_length=300 , widget=forms.TextInput(attrs={'id':'address','class':'text_field'}) )
	old_password = forms.CharField(label='Old password',widget=forms.PasswordInput(attrs={'id':'old_password','class':'text_field'}))
	new_password = forms.CharField(label='New password',widget=forms.PasswordInput(attrs={'id':'new_password','class':'text_field'}))
	conf_password = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'id':'conf_password','class':'text_field'}))
