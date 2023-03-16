from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.contrib.auth import logout

# User Signout function
def user_signout(request):
    logout(request)
    return HttpResponseRedirect('/signin')

# User Sign in function
def user_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticating user
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Account is Disabled")
        else:
            return HttpResponse('Invalid Login')
    else:
        return render(request, 'socialapp/signin.html')

# Registering New user using Django Forms
def register(request):
    registered = False
    
    if request.method == 'POST':
        # Getting user data from the form and saving the new user
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'occupation' in user_form.cleaned_data:
                profile.organisation = request.DATRA['occupation']
            profile.save()
            registered = True
            friend = Friends.objects.create(user=user)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'socialapp/signup.html', {'user_form': user_form, 
                                                      'profile_form': profile_form, 
                                                      'registered': registered})

# Rendering the home page which is the profile of the logged in user
@login_required
def home(request):
    user = request.user
    posts = UserPost.objects.filter(user=user).order_by('-date_created')
   
    return render(request, 'socialapp/index.html', {'posts': posts})

# Function for user to edit their data such as images, occupation and bio
@login_required
def user_edit(request):
    user = request.user.appuser
    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'socialapp/edit.html', context)

# Search function enabling the user to get all the other user
@login_required
def search(request):
    # getting the current user
    user_object = User.objects.get(username=request.user.username)
    user_profile = AppUser.objects.get(user=user_object)
    username_profile_list = []
    username_profile =  []
    
    if request.method == 'POST':
        # checking if POST, then take the query and filter using the words written
        username = request.POST['q']
        username_object = User.objects.filter(username__icontains=username)
        
        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = AppUser.objects.filter(user_id=ids)
            username_profile_list.append(profile_lists)
            
        # Chaining the list to display the results after
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'socialapp/search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

# Profile fuction to show the profile of other users including friends and people who are not friends
@login_required
def profile(request, pk):
    # If user clicks on their own profile or searches themselves, then gets redirected to home
    user_object = User.objects.get(username=pk)
    if user_object == request.user:
        return redirect('/')
    else:
        # Getting all the relevant data of other user
        profile = AppUser.objects.get(user=user_object)
        friend = Friends.objects.get(user=request.user)
        friends = friend.friends.all()
        
        # Checking if we have an active friend request with them
        req_status = FriendRequest.objects.filter(sender=request.user, receiver=user_object).exists()
        
        # Checking if we are friends with the user
        if profile.user in friends:
            status = True
        else:
            status = False
        # Getting posts of the user and ordering them by the data created from newest to oldest
        posts = UserPost.objects.filter(user=user_object).order_by('-date_created')
        return render(request, 'socialapp/profile.html', {'user_object': user_object, 'profile': profile, "posts": posts, "status": status, "req_status": req_status})

# Adding a post as a current user
@login_required
def addpost(request):
    if request.method == 'POST':
        # Getting the image from the front end and the description
        post_image = request.FILES.get('post_image')
        description = request.POST['description']
        # Saving it as current user's post
        add_post = UserPost.objects.create(user=request.user, post_image=post_image, description=description)
        add_post.save()
        return render(request, 'socialapp/addpost.html')
    else:
        return render(request, 'socialapp/addpost.html')

# Function delete's the post of the current user
@login_required
def deletepost(request, pk):
    delete_post = UserPost.objects.get(id=pk)
    delete_post.delete()
    return redirect('/')

# Function handling the friend request   
@login_required
def friendrequest(request, pk):
    # Getting the id of the other user and generating friend request if it doesn't exist
    sender = request.user
    recipient = User.objects.get(username=pk)
    model = FriendRequest.objects.get_or_create(sender=sender, receiver=recipient)
    return redirect('/')

# Function enabling the reciever to delete the friend request they recieved
@login_required
def delete_friend_req(request, pk):
    friend = User.objects.get(username=pk)
    f_req = FriendRequest.objects.get(sender=friend, receiver=request.user)
    f_req.delete()
    return redirect('/requests/')

# Function printing all the requests the user recieved
@login_required
def requests(request):
    requests = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'socialapp/requests.html', {'requests': requests})

# Function for accepting the friend request and adding as friends
@login_required
def add_friends(request, pk):
    friend = User.objects.get(username=pk)
    f_req = FriendRequest.objects.get(sender=friend, receiver=request.user)
    
    # calling the custom function
    new_friend = Friends.add_friend(request.user, friend)
    new_friend = Friends.add_friend(friend, request.user)
    f_req.delete()
    
    return redirect('/requests/')


# Removing the existing friend!
@login_required
def delete_friends(request, pk):
    friend = User.objects.get(username=pk)    
    new_friend = Friends.remove_friend(request.user, friend)
    new_friend = Friends.remove_friend(friend, request.user)

    return redirect('/allfriends/')

# Showing the existing friends of the logged in user
@login_required
def all_friends(request):
    
    friend = Friends.objects.get(user=request.user)
    friends = friend.friends.all()
    return render(request, 'socialapp/friendlist.html', {'friends': friends})

# Function to handle the chat room
@login_required
def room(request, room_name):
    return render(request, 'socialapp/room.html', {'room_name': room_name })
