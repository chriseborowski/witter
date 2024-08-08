from django.shortcuts import render
from .models import UserProfile

# Create your views here.
def home(request):
  return render(request, 'home.html', {})

def profile_list(request):
  profiles = UserProfile.objects.exclude(user=request.user)

  return render(request, 'profile_list.html', {"profiles": profiles})
