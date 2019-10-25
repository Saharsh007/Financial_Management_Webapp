
from django import forms
from app1.models import UserProfileInfo
from django.contrib.auth.models import User
from app1.models import CurrentTransaction


class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('name','gender','dob')

class TransactionForm(forms.Form):
	Email=forms.EmailField(label='Email',max_length=50)
	Amount=forms.IntegerField(label='Amount')
	Action=forms.ChoiceField(choices=[('Lent','Lent'),('Borrowed','Borrowed')])
	Desc=forms.CharField(label='Description',max_length=20)
