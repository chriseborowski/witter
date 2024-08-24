from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create a witt (posts) model

class Witt(models.Model):
  user = models.ForeignKey(
    User, 
    related_name="witts", 
    on_delete=models.DO_NOTHING)
  body = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  likes = models.ManyToManyField(User, related_name="witt_like", blank=True)

  # Count likes
  def number_of_likes(self):
    return self.likes.count()

  def __str__(self):
    return(
      f"{self.user} "
      f"({self.created_at:%d-%m-%Y at %H:%M}): "
      f"{self.body}..."
    )

# Create a user profile model

class UserProfile(models.Model):

  # Set a one-to-one relationship between each user and their profile
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  
  # Allow for many-to-many relationships between profiles
  follows = models.ManyToManyField("self",
  related_name="followed_by",
  symmetrical=False, # Set asymmetrical user-to-user following relationship
  blank=True) # Allow user not to follow anyone

  # Update date modified when profile is updated
  date_modified = models.DateTimeField(User, auto_now=True)
  profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
  profile_bio = models.CharField(null=True, blank=True, max_length=500)

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
