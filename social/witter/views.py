from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile, Witt
from .forms import WittForm, SignUpForm, ProfileUpdateForm, ProfilePictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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
    profile = UserProfile.objects.get(user__id=pk)
    witt = Witt.objects.filter(user__id=pk).order_by('-created_at')

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
  logout(request)
  messages.success(request, ("You have been logged out."))
  return redirect('home')


def register_user(request):
  form = SignUpForm()
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      # Log in user
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, ("You have successfully registered. Welcome to Witter!"))
      return redirect('home')
  else:
    form = SignUpForm()
  return render(request, 'register.html', {'form': form})


def update_user(request):
  if request.user.is_authenticated:
    current_user = UserProfile.objects.get(user__id=request.user.id)
    profile_user = UserProfile.objects.get(user__id=request.user.id)
    
    # Get forms
    user_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=current_user)
    profile_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=profile_user)
    
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      # login(request, current_user)
      messages.success(request, ("Your profile has been updated."))
      return redirect('home')
    return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form})
  else:
    messages.success(request, ("You must be logged in to view this page"))
    return redirect('home')


def witt_like(request, pk):
  if request.user.is_authenticated:
    witt = get_object_or_404(Witt, id=pk)
    if witt.likes.filter(id=request.user.id).exists():
      witt.likes.remove(request.user)
    else:
      witt.likes.add(request.user)
    return redirect(request.META.get("HTTP_REFERER"))
  else:
    messages.success(request, ("You must be logged in to view this page."))
    return redirect('home')


def witt_show(request, pk):
  witt = get_object_or_404(Witt, id=pk)
  if witt:
    return render(request, 'show_witt.html', {'witt': witt})
  else:
    messages.success(request, ("That witt does not exist."))
    return redirect('home')


def followers(request, pk):
  if request.user.is_authenticated:
    if request.user.id == pk:
      profiles = UserProfile.objects.get(user__id=pk)
      return render(request, 'followers.html', {'profiles': profiles, 'followers': followers})
    else:
      messages.success(request, ("You cannot access this page. You will be redirected to the home page shortly."))
      return redirect('home')
  else:
    messages.success(request, ("You must be logged in to view this page"))
    return redirect('home')


def following(request, pk):
  if request.user.is_authenticated:
    if request.user.id == pk:
      profiles = UserProfile.objects.get(user__id=pk)
      return render(request, 'following.html', {'profiles': profiles, 'following': following})
    else:
      messages.success(request, ("You cannot access this page. You will be redirected to the home page shortly."))
      return redirect('home')
  else:
    messages.success(request, ("You must be logged in to view this page"))
    return redirect('home')


def delete_witt(request, pk):
  if request.user.is_authenticated:
    witt = get_object_or_404(Witt, id=pk)
    if request.user.username == witt.user.username:
      witt.delete()
      messages.success(request, ("Your witt has been deleted."))
      return redirect(request.META.get("HTTP_REFERER"))
    else:
      messages.success(request, ("You are not authorized to perform this action."))
      return redirect('home')
  else:
    messages.success(request, ("You must be logged in to view this page"))
    return redirect(request.META.get("HTTP_REFERER"))


def search(request):
  if request.method == "POST":
    search = request.POST['search']
    searched = Witt.objects.filter(body__contains=search)
    return render(request, 'search.html', {'search': search, 'searched': searched})
  else:
    return render(request, 'search.html', {})


def search_user(request):
  if request.method == "POST":
    search = request.POST['search']
    searched = User.objects.filter(username__contains=search)
    return render(request, 'search_user.html', {'search': search, 'searched': searched})
  else:
    return render(request, 'search_user.html', {})
