from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	balance=models.IntegerField(default=0)
	def __str__(self):
		return self.user.username
