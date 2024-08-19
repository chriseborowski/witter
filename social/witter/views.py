from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, Witt
from .forms import WittForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
  witts = None
  if request.user.is_authenticated:
    form = WittForm(request.POST or None)
    if request.method == "POST":
      if form.is_valid():
        witt = form.save(commit=False)
        witt.user = request.user
        witt.save()
        messages.success(request, ("Your witt has been posted!"))
        return redirect('home')

    witts = Witt.objects.all().order_by('-created_at')
    return render(request, 'home.html', {"witts":witts, "form":form})
  else:
    witts = Witt.objects.all().order_by('-created_at')
    return render(request, 'home.html', {"witts":witts})

def profile_list(request):
  if request.user.is_authenticated:
    profiles = UserProfile.objects.exclude(user=request.user)
    return render(request, 'profile_list.html', {"profiles": profiles}) # Ensure that only logged in users can display user profiles
  else:
    messages.success(request, ("You must be logged in to view this page"))
    return redirect('home')

def profile(request, pk):
  if request.user.is_authenticated:
    profile = UserProfile.objects.get(user_id=pk)
    witt = Witt.objects.filter(user_id=pk).order_by('-created_at')

    # Follow/Unfollow logic using POST
    if request.method == "POST":
      current_user_profile = request.user.profile
      action = request.POST['follow']
      if action == "unfollow":
        current_user_profile.follows.remove(profile)
      else:
        current_user_profile.follows.add(profile)
      current_user_profile.save()
    
    return render(request, 'profile.html', {"profile": profile, "witts":witt})
  else:
    messages.success(request, ("You must be logged in to view this page"))
    return redirect('home')


def login_user(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      messages.success(request, ("You have been logged in."))
      return redirect('home')
    else:
      messages.success(request, ("There was an error logging in. Please try again."))
      return redirect('login')

  else:
    return render(request, 'login.html', {})


def logout_user(request):
  pass
