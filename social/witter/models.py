from django.db import models
from django.contrib.auth.models import User

# Create a user profile model

class UserProfile(models.Model):

  # Set a one-to-one relationship between each user and their profile
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  
  # Allow for many-to-many relationships between profiles
  follows = models.ManyToManyField("self",
  related_name="followed_by",
  symmetrical=False, # Set asymmetrical user-to-user following relationship
  blank=True) # Allow user not to follow anyone

  def __str__(self):
    return self.user.username
