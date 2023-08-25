from rest_framework import serializers
from .models import *
# from passlib.hash import django_pbkdf2_sha256 as handler
from passlib.hash import django_pbkdf2_sha256 as handler



class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users 
        fields = ['username', 'fname', 'lname', 'email', 'password']
        
    def validate_email(self, val):
        if Users.objects.filter(email=val).exists():
            raise serializers.ValidationError("Email Already Exist . . .")
        return val
        
        
    def validate_username(self, val):
        if Users.objects.filter(username = val).exists():
            raise serializers.ValidationError("Username already exist . . . ")
        return val
        
        
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        if len(password) < 8 or len(password) > 16:
            raise serializers.ValidationError("Password length must be 8 to 20 char")
        
        validated_data['password'] = handler.hash(password)
        return super().create(validated_data)
        


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "password"]
        
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if "@" in username:
            fetchuser = Users.objects.filter(email = username).first()
            if not fetchuser:
                raise serializers.ValidationError("No email Found !!!")
        
        else:
            fetchuser = Users.objects.filter(username =username).first()
            if not fetchuser:
                raise serializers.ValidationError("No usermane was found !!!")
            
        check_pass=  handler.verify(password, fetchuser.password)
        
        if not check_pass:
                raise serializers.ValidationError("Password Not Correct !!!!")
      
        return attrs
        
        
        
        