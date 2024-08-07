from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import UserProfile

# Unregistering groups
admin.site.unregister(Group)

# Connect user profiles to users
class ProfileInline(admin.StackedInline):
  model = UserProfile

# Extending User model
class UserAdmin(admin.ModelAdmin):
  model = User

  fields = ["username"]
  inlines = [ProfileInline]

# Unregistering initial User
admin.site.unregister(User)

# Reregistering User and UserProfile
admin.site.register(User, UserAdmin)
# admin.site.register(UserProfile)

