from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create a user profile model

class UserProfile(models.Model):

  # Set a one-to-one relationship between each user and their profile
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  
  # Allow for many-to-many relationships between profiles
  follows = models.ManyToManyField("self",
  related_name="followed_by",
  symmetrical=False, # Set asymmetrical user-to-user following relationship
  blank=True) # Allow user not to follow anyone

  # Update date modified when profile is updated
  date_modified = models.DateTimeField(User, auto_now=True)

  def __str__(self):
    return self.user.username

# Create a user profile when a new user signs up
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
  if created:
    user_profile = UserProfile(user=instance)
    user_profile.save()

    # Have the user follow themselves
    user_profile.follows.add(user_profile)
    user_profile.save()

post_save.connect(create_profile, sender=User)
