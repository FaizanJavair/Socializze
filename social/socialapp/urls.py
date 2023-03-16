from django.urls import include, path
from django.contrib.auth.decorators import login_required
from . import views
from . import api

urlpatterns = [
    path('', login_required(login_url='signin')( views.home), name='home'), # Path to home if user is logged in // VIEW
    path('register/', views.register, name='register'), # Path to registering if user doesn't exist // VIEW
    path('signin/', views.user_signin, name='signin'), # Path to sign in page // VIEW
    path('signout/', views.user_signout, name='signout'), # Path to sign out frmo user account // VIEW
    path('edit/', login_required(login_url='signin')( views.user_edit), name='edit'), # Path to edit the user information // VIEW
    path('search/', login_required(login_url='signin')( views.search), name='search'), # Path to Searching a user // VIEW
    path('addpost/', login_required(login_url='signin')( views.addpost), name='addpost'), # Path to Adding a user post // VIEW
    path('deletepost/<str:pk>', login_required(login_url='signin')( views.deletepost), name='deletepost'), # Path to deleting the user post // VIEW
    path('profile/<str:pk>', login_required(login_url='signin')( views.profile), name='profile'), # Path to other user profile // VIEW
    path('sendrequest/<str:pk>', login_required(login_url='signin')( views.friendrequest), name='request'), # Path to sending a friend request // VIEW
    path('requests/', login_required(login_url='signin')( views.requests), name='requests'), # Path to showing all the requests // VIEW
    path('request/accept/<str:pk>', login_required(login_url='signin')( views.add_friends), name='addriends'), # Path to accepting th user request // VIEW
    path('request/delete/<str:pk>', login_required(login_url='signin')( views.delete_friend_req), name='delete_friend_req'), # Path to deleteing friend request // VIEW
    path('unfriend/<str:pk>', login_required(login_url='signin')( views.delete_friends), name='delete_friends'), #Path to unfriending a friend // VIEW
    path('allfriends/', login_required(login_url='signin')( views.all_friends), name='all_friends'), # Path to displaying all the user friends
    path('chat/<str:room_name>/',login_required(login_url='signin')( views.room), name='room'), # Path to chat room
    path('api/user/',login_required(login_url='signin')( api.user_profile), name='user_profile'), # // API //  User profile data 'GET'
    path('api/user/<str:pk>',login_required(login_url='signin')( api.UserDetail.as_view()), name='user_profile_update'), # // API //  user profile data 'GET', 'PUT'
    path('api/user/posts/',login_required(login_url='signin')( api.user_posts), name='user_posts'), # // API // all user posts 'GET'
    path('api/user/posts/<str:pk>',login_required(login_url='signin')( api.PostDetail.as_view()), name='user_post'), # // API //  user post 'GET', 'POST', 'DELETE'
    path('api/user/friends/',login_required(login_url='signin')( api.user_friends), name='user_friends'), # // API //  all user friends 'GET'
    path('api/user/profile/<str:pk>',login_required(login_url='signin')( api.all_user_profile), name='all_user_profile'), # // API // specific user all data 'GET'
    
]