from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class AuthUserSerializer(serializers.ModelSerializer):
	auth_token = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('id','username','auth_token')

	def get_auth_token(self, obj):
		Token.objects.filter(user=obj).delete()
		token = Token.objects.create(user=obj)
		return token.key


class EmptySerializer(serializers.Serializer):
	pass
