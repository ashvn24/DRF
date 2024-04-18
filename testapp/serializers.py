from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,write_only =True)
    password = serializers.CharField(write_only=True, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields ='__all__'
        