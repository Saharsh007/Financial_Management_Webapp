from django.db import models
from django.contrib.auth.models import User
# Create your models here.

User._meta.get_field('email')._unique = True
class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	dob=models.DateField()
	gender=models.CharField(max_length=10)
	name=models.CharField(max_length=20,default='DefaultName')
	def __str__(self):
  		return self.user.username

class CurrentTransaction(models.Model):
	user_id1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related1')
	user_id2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related2')

	tdate=models.DateTimeField()
	amount=models.IntegerField()
	lent=models.CharField(max_length=30)
	borrowed=models.CharField(max_length=30)
	desc=models.CharField(max_length=100)

class Friends(models.Model):
	user_id1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related1')
	user_id2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related2')
	class Meta:
		unique_together = ['user_id1', 'user_id2']

class TransactionHistory(models.Model):
	user_id=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateField()
	Amount=models.IntegerField()
	lent=models.CharField(max_length=30)
	borrowed=models.CharField(max_length=30)
	Desc=models.CharField(max_length=100)








