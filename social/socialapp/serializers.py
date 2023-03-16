from rest_framework import serializers
from .models import *

# User serializer to get user data from standard django model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# User serializer from the custom model we made that extends to Standard User model
class UserDataSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AppUser
        fields = ['id', 'user', 'occupation', 'date_joined', 'last_login', 'profile_image', 'bio']

# User serializer to just show the data from custom user model and update data using this in the API
class UserUpdateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'user', 'occupation', 'date_joined', 'last_login', 'profile_image', 'bio']

# User Post serializer to show all the user posts 
class UserPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['id','description', 'post_image']

# User Post serializer to create and delete using class based API view
class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['id','user', 'description', 'post_image']

# User friends serializer to show all the existing friend of the current user 
class UserFriendsSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True)
    user = UserSerializer(many=False)
    class Meta:
        model = Friends
        fields = ['user','friends']