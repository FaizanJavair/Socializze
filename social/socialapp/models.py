from django.db import models
from django.contrib.auth.models import User
import os
import uuid

# Custom user model that extends the standard django user
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=256, verbose_name='occupation', null = True, blank = True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, default="defaultImage.png", upload_to='profile_img')
    bio = models.CharField(max_length=500, null=True, blank=True)
    
    # Returning username
    def __str__(self):
        return self.user.username

# Function that makes sure the file path is always unique when saved to avoid duplicate data not posting
def get_file_path(self, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(uuid.uuid4()), ext)
    return os.path.join('post_img', filename)

# User Post data
class UserPost(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, null=True, blank=True)
    post_image = models.FileField(null=True, blank=True, upload_to=get_file_path) # above function gets called here
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    
    # Returning the username
    def __str__(self):
        return self.user.username

# Friends model that extends the User model to make friends with many to many relationship
class Friends(models.Model):
    user = models.OneToOneField(User, related_name='owner', on_delete=models.CASCADE, null=True)
    friends = models.ManyToManyField(User, related_name='friend')
    
    # Returning user username
    def __str__(self):
        return self.user.username
    
    # Custom class method that is called in the VIEW to create new friends
    @classmethod
    def add_friend(self, user, new_friend):
        friend, create=self.objects.get_or_create(
            user=user
        )
        friend.friends.add(new_friend)
    # Custom class method that is called in the VIEW to delete the existing friend
    @classmethod
    def remove_friend(self, user, new_friend):
        friend, create = self.objects.get_or_create(
            user=user
        )
        friend.friends.remove(new_friend)
    
# Friend request model to save any friend request
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, null=True, related_name='send', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    # Returning sender's username
    def __str__(self):
        return self.sender.username