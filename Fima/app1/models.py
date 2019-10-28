from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import RegexValidator
# Create your models here.

User._meta.get_field('email')._unique = True
class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	dob=models.DateField()
	Categories =(("Male","Male"),("Female","Female"))
	gender=models.CharField(max_length=10 , choices=Categories)
	name=models.CharField(max_length=20,default='Your Name')		
	profile_pic = models.ImageField(upload_to='app1/profile_pics',blank=True,default='app1/profile_pics/default.png')
	phone_number = models.CharField(max_length=10,blank=True,validators=[RegexValidator('^[0-9]{10}$',message="Invalid Number")])
	user_address=models.CharField(max_length=300,blank=True)
	def __str__(self):
  		return self.user.username

class CurrentTransaction(models.Model):
	user_id1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related1')
	user_id2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related2')
	tdate=models.DateField()
	amount=models.IntegerField()
	lent=models.CharField(max_length=30)
	borrowed=models.CharField(max_length=30)
	desc=models.CharField(max_length=400)

class Friends(models.Model):
	user_id1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related1')
	user_id2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related2')
	class Meta:
		unique_together = ['user_id1', 'user_id2']

class TransactionHistory(models.Model):
	user_id1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related1')
	user_id2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related2')
	date=models.DateField()
	Amount=models.IntegerField()
	lent=models.CharField(max_length=30)
	borrowed=models.CharField(max_length=30)
	Desc=models.CharField(max_length=400)

class OldNotification(models.Model):
	user_id=models.ForeignKey(User,on_delete=models.CASCADE)
	desc=models.CharField(max_length=400)
	date=models.DateField()

class NewNotification(models.Model):
	user_id=models.ForeignKey(User,on_delete=models.CASCADE)
	desc=models.CharField(max_length=400)
	date=models.DateField(default=datetime.date.today)


#yes





