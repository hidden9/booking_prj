from rest_framework import serializers
from userAuth.models import User


# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
   def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_customer=validated_data['is_customer'],
            is_room_manager=validated_data['is_room_manager']
        )
        user.set_password(validated_data['password'])
        user.save()
        user.password = '**hidden**'
        return user

