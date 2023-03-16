import factory

from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *
from django.contrib.auth.models import User

# ////////////////////////////////////////////////////////////
# MODEL FACTORY FOR THE TESTS WHICH IS USED TO MAKE DUMMY DATA
# ///////////////////////////////////////////////////////////

class UserFactory(factory.django.DjangoModelFactory):
    username = "test"
    email = "test@123.com"
    password = "test123"
    
    class Meta:
        model = User
        
class AppUserFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    occupation = "web developer"
    bio = "I am a User!"
    
    class Meta:
        model = AppUser
        
class UserPostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    description = "wow, I made a post!"
    
    class Meta:
        model = UserPost
