from django.contrib import admin
from django.contrib.auth.models import Group

# Unregistering groups
admin.site.unregister(Group)
