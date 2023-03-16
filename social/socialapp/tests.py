import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.test import Client
from .model_factories import *
from .serializers import *
from django.contrib.auth import authenticate, login
# Testing user and their data serializers 
class UserDataSerializerTest(APITestCase):
    # for user from USER MODEL
    user = None
    userserializer = None
    # for appuser from CUSTOM APPUSER MODEL
    appuser = None
    appuserserializer = None
    # for userposts form CUSTOM USERPOST MODEL
    userpost = None
    userpostserializer = None
    def setUp(self):
        self.user = UserFactory.create(pk=1, username='test')
        self.appuser = AppUserFactory.create(pk=1, user=self.user)
        self.userpost = UserPostFactory.create(pk=1, user=self.user)
        self.userserializer = UserSerializer(instance=self.user)
        self.appuserserializer = UserDataSerializer(instance=self.appuser)
        self.userpostserializer = UserPostSerializer(instance=self.userpost)
    
    # Clearing the data after test's are done running
    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        UserPost.objects.all().delete()
        Friends.objects.all().delete()
    
    # Testing the user serialzier
    def test_userSerializerHasCorrectFields(self):
        data = self.userserializer.data
        self.assertEqual(set(data.keys()), set(['id','username','email']))
    
    def test_userSerializerHasGoodData(self):
        data = self.userserializer.data
        self.assertEqual(data['username'], 'test')
        self.assertEqual(data['email'], 'test@123.com')
    
    # Testing the app user serializer
    def test_appuserSerializerHasCorrectFields(self):
        data = self.appuserserializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'occupation', 'date_joined', 'last_login', 'profile_image', 'bio']))
        
    def test_appuserSerializerHasGoodData(self):
        data = self.appuserserializer.data
        self.assertEqual(data['occupation'], 'web developer')
        self.assertEqual(data['bio'], 'I am a User!')
    
    # Testing user post serializer
    def test_userPostSerializerHasCorrectFields(self):
        data = self.userpostserializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'description', 'post_image']))
        
    def test_userPostSerializerHasGoodData(self):
        data = self.userpostserializer.data
        self.assertEqual(data['description'], 'wow, I made a post!')

# Checking if user can be created and can be logged in
class UserAuthTest(TestCase):
    user = None
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.user.save()
        
    # Clearing the data after test's are done running
    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        UserPost.objects.all().delete()
    
    def test_correctInfo(self):
        user = authenticate(username='test', password='test123')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrongInfo_username(self):
        user = authenticate(username='wrong', password='test123')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrongInfor_password(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

# Testing most of the PATHS since they all require login
class UserDataAuthViewTest(APITestCase):
    user = None
    user1 = None
    appuser = None
    post = None
    new_friend = None
    def setUp(self):
        # Dummy login created
        self.user = User.objects.create_user(username='test', password='test123')
        self.user1 = User.objects.create_user(username='test1', password='test123')
        self.user.save()
        self.client.login(username='test', password='test123')
        self.appuser = AppUserFactory.create(user=self.user)
        self.post = UserPostFactory.create(user=self.user)
        # calling the custom function
        self.new_friend = Friends.add_friend(self.user, self.user1)
        self.new_friend = Friends.add_friend(self.user1, self.user)
        
        
    # Clearing the data after test's are done running
    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        UserPost.objects.all().delete()
        Friends.objects.all().delete()
    
    # Testing home page with good and bad url
    def test_homePageGet(self):
        response = self.client.get('/', format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_homePageNotGet(self):
        response = self.client.get('/sdasd', format="json")
        self.assertEqual(response.status_code, 404)
    
    # Testing search results wiht good and bad url
    def test_searchPageGet(self):
        response = self.client.get('/search/?q=test', format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_searchPageNotGet(self):
        response = self.client.get('/sarch', format="json")
        self.assertEqual(response.status_code, 404)
    
    # Testing all request page with good and bad URL
    def test_requestPageGet(self):
        response = self.client.get('/requests', format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_requestPageGet(self):
        response = self.client.get('/requestssd', format="json")
        self.assertEqual(response.status_code, 404)
    
    # Testing allfriends with good and bad url
    def test_allFriendsPageGet(self):
        response = self.client.get('/allfriends/', format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_allFriendsPageNotGet(self):
        response = self.client.get('/allfrien', format="json")
        self.assertEqual(response.status_code, 404)
 
    # Testing API user data get endpoint good and bad URL
    def test_apiUserPageGet(self):
        response = self.client.get('/api/user/', format="json")
        self.assertEqual(response.status_code, 200)
      
    def test_apiUserPageNotGet(self):
        response = self.client.get('/api/users', format="json")
        self.assertEqual(response.status_code, 404)
    
    # Testing API other user profile using good and bad URL   
    def test_apiUserProfilePageGet(self):
        response = self.client.get('/api/user/profile/test', format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_apiUserProfilePageNotGet(self):
        response = self.client.get('/api/users/prof', format="json")
        self.assertEqual(response.status_code, 404)
        
    # Testing API friends profile using good and bad URL   
    def test_apiUserFriendsPageGet(self):
        response = self.client.get('/api/user/friends/', format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_apiUserFriendsPageNotGet(self):
        response = self.client.get('/api/user/friend/', format="json")
        self.assertEqual(response.status_code, 404)
    
    # Testing API post of user with good and bad URL 
    def test_apiUserPostPageGet(self):
        response = self.client.get('/api/user/posts/1', format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_apiUserPostPageNotGet(self):
        response = self.client.get('/api/user/posts/g', format="json")
        self.assertEqual(response.status_code, 404)
    
    # Testing API all posts get with good and bad url
    def test_apiUserAllPostPageGet(self):
        response = self.client.get('/api/user/posts/', format="json")
        self.assertEqual(response.status_code, 200)
       
    def test_apiUserAllPostPageNotGet(self):
        response = self.client.get('/api/user/post/', format="json")
        self.assertEqual(response.status_code, 404)
        
    # Testing API to get specific user  with  bad url
    def test_apiUserDataPageNotGet(self):
        response = self.client.get('/api/user/kratos', format="json")
        self.assertEqual(response.status_code, 404)
    
    # Testing chatroom with Bad URL
    def test_chatRoomPageNotGet(self):
        response = self.client.get('chats/hello', format="json")
        self.assertEqual(response.status_code, 404)
        
    
   
    

    