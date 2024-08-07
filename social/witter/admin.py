from django.contrib import admin
from django.contrib.auth.models import Group, User

# Unregistering groups
admin.site.unregister(Group)

# Extending User model
class UserAdmin(admin.ModelAdmin):
  model = User

  fields = ["username"]

# Unregistering initial User
admin.site.unregister(User)

# Reregistering User
admin.site.register(User, UserAdmin)
