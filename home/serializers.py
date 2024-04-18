from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User




# Serializer for user registration
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("username is taken")
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("email is taken")
              
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'], 
            email = validated_data['email']
        )      
        user.set_password(validated_data['password'])
        user.save()
        return validated_data




# Custom serializer by not using ModelSerializer class
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    


# This serializer will only show the data we want to display from foreign table
class ColorSerializer(serializers.ModelSerializer):
     class Meta:
          model = Color
          fields = ['color_name']


class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only = True)
    class Meta:
        model = Person
        fields = '__all__'
        # fields = ['name', 'age']    for selected fields
        # exclude = ['name', 'age']    it will exclude these fields only
        # depth = 1    used to show all data from foreign key connected table



    def validate(self, data):
            # name validation
            special_chars = "!@#$%^&*()-+_=,<>/"
            # if any(c in special_chars for c in data['name']):
            #      raise serializers.ValidationError('name cannot contain special characters')

            # # age validation
            # if data['age'] < 18:
            #     raise serializers.ValidationError('age shoule be greater than 18')
            
            return data
    






