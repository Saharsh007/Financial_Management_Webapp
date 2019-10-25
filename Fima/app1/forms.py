# from django import forms
# from app1.models import UserProfileInfo
# from django.contrib.auth.models import User
# from app1.models import CurrentTransaction

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta():
#         model = User
#         fields = ('email','password')


# class UserProfileInfoForm(forms.ModelForm):
#      class Meta():
#          model = UserProfileInfo
#          fields = ('name','gender','dob')

# class TransactionForm(forms.Form):
# 	Email=forms.EmailField(label='Email',max_length=20)
# 	Amount=forms.IntegerField(label='Email',max_length=20)
# 	Action=forms.ChoiceField(choices=['Lent','Borrowed'])
# 	Desc=forms.CharField(label='Email',max_length=20,)
