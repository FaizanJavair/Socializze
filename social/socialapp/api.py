from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

from django.contrib.auth.decorators import login_required

# API function to get the current logged in user data
@login_required
@api_view(['GET', 'POST'])
def user_profile(request):
    if request.method == 'POST':
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user_object = ''
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = AppUser.objects.get(user=user_object)
        print(user_object)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        
       serializer = UserDataSerializer(user_profile)
       return Response(serializer.data)

# API view to get the current logged in user posts
@login_required
@api_view(['GET'])
def user_posts(request):
    user_object = ''
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = UserPost.objects.filter(user=user_object)
        print(user_object)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
       user_serializer = UserSerializer(user_object)
       serializer = UserPostsSerializer(user_profile, many=True)
       context = {
           "user": user_serializer.data,
           "posts": serializer.data
       }
       return Response(context)

# API function to get all the current logged in user friends
@login_required
@api_view(['GET'])
def user_friends(request):
    user_object = ''
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Friends.objects.filter(user=user_object)
        print(user_object)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
       serializer = UserFriendsSerializer(user_profile, many=True)

       return Response(serializer.data[0])

# API function to get the profile and relevant data of existing user on the APP
@login_required
@api_view(['GET'])
def all_user_profile(request, pk):
    user_object = ''
    try:
        user_object = User.objects.get(username=pk)
        user_profile = UserPost.objects.filter(user=user_object)
        print(user_object)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
       user_serializer = UserSerializer(user_object)
       serializer = UserPostsSerializer(user_profile, many=True)
       context = {
           "user": user_serializer.data,
           "posts": serializer.data
       }
       return Response(context)

# API class based view to GET, POST, and DELETE the user posts
class PostDetail(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# API Class based views to edit and get certain user data
class UserDetail(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserUpdateDataSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
