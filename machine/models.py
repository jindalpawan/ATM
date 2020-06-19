from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
	user= models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	balance=models.IntegerField(default=0)
	def __str__(self):
		return self.balance

class Transaction(models.Model):
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	amount=models.IntegerField(default=0)
	time= models.DateTimeField(auto_now_add= True)
	types= models.CharField(max_length= 10) 