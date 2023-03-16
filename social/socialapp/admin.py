from django.contrib import admin
from .models import *

# Registering all the models
admin.site.register(AppUser)
admin.site.register(UserPost)
admin.site.register(Friends)
admin.site.register(FriendRequest)

