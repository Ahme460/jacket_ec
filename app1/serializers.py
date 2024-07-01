from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from .models import *

User = get_user_model()
class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','username', 'email', 'password','password2')

        extra_kwargs = {
            'first_name': {'required':True ,'allow_blank':False},
            'username' : {'required':True ,'allow_blank':False},
            'email' : {'required':True ,'allow_blank':False},
            'password' : {'required':True ,'allow_blank':False,'min_length':8}
        }
        def validate(self, data):


            password1 = data.get('password')
            password2 = data.get('password2')
            email=data.get('email')
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email is used")
            if password1 != password2:
                raise serializers.ValidationError("Passwords do not match.")
            return data
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'username') 




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                data['user'] = user
            else:
                raise AuthenticationFailed('Invalid login credentials')
        else:
            raise AuthenticationFailed('Must include "email" and "password"')
        return data
    



class ProductSerializer_detal(serializers.ModelSerializer):
    class meta:
        models = Products
        fields= ('details','name','price')





class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields =  ['id', 'product', 'quantity', 'user', 'size', 'color', 'date_added']
        extra_kwargs = {
            'product': {'required': True},
            'quantity': {'required': True},
            'user': {'required': True},
            'size': {'required': True},
            'color': {'required': True},
        }


