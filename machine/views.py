from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import os
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Account
from rest_framework.views import APIView
from .utils import get_and_authenticate_user
from rest_framework import viewsets
import json


# Current notes in the ATM.  
n2000=0
n500=0
n200=0
n100=0
AtmAmount=0  # current amount in the ATM


# Deposite amount in the Account
class Deposite(APIView):	
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		data=json.dumps(request.data)
		data=json.loads(data)
		amount=data["amount"]
		if amount%100==0:
			user=request.user
			user.balance=user.balance+amount
			AtmAmount=AtmAmount+amount
			n2000=n2000+data["n2000"]
			n500=n500+data["n500"]
			n200=n200+data["n200"]
			n100=n100+data["n100"]
			dic={'Error':"success"}
		else:
			dic={'Error':"amount should be multiple by 100"}
		return Response(dic)


#Withdraw money
class Withdraw(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		data=json.dumps(request.data)
		data=json.loads(data)
		amount=data["amount"]
		user=request.user
		dic={}
		if amount>20000:
			dic["Error"]="Not enough cash in your account"
		else:
			if user.balance>=amount:
				if AtmAmount>=amount:
					if amount%100==0:
						user.balance=user.balance- amount
						
						#couunt how many notes of 20000 will require
						if n2000:
							x=amount/2000
							n2000=n2000-x
							amount=amount%2000
							dic["n2000"]=x

						if amount>=(500*n500):
							x=amount/500
							n500=n500-x
							amount=amount%500
							dic["n500"]=x

						if amount>=(200*n200):
							x=amount/200
							n200=n200-x
							amount=amount%200
							dic["n200"]=x

						if amount>=(100*n100):
							x=amount/100
							n100=n100-x
							amount=amount%100
							dic["n100"]=x
					else:
						dic["Error"]="Amount shuold be multiple of Rs100"
				else:
					dic["Error"]="Not enough cash in ATM"
			else:
				dic["Error"]="Not enough cash in your account"	

		return Response(dic)


class AuthViewSet(viewsets.ViewSet):

	permission_classes = [AllowAny, ]
	
	@action(methods=['POST', ], detail=False)
	def login(self, request):
		data=json.dumps(request.data)
		data=json.loads(data)
		userlength=len(data["username"])
		passlength=len(data["password"])
		if userlength==8 and passlength==4:
			user = get_and_authenticate_user(data["username"], data["password"])
			data = serializers.AuthUserSerializer(user).data
			return Response(data=data, status=status.HTTP_200_OK)
		else:
			dic={'Error':"username and password not matched"}
			return Response(dic)

	@action(methods=['GET', ], detail=False)
	def logout(self, request):
		if request.user.is_authenticated:
			request.user.auth_token.delete()
			data = {'success': 'Sucessfully logged out'}
		else:
			data = {'Error': 'Have not token'}
		return Response(data=data, status=status.HTTP_200_OK)