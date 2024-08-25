from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('profile_list/', views.profile_list, name='profile_list'),
  path('profile/<int:pk>', views.profile, name='profile'),
  path('profile/followers/<int:pk>', views.followers, name='followers'),
  path('profile/following/<int:pk>', views.following, name='following'),
  path('login/', views.login_user, name='login'),
  path('logout/', views.logout_user, name='logout'),
  path('register/', views.register_user, name='register'),
  path('update_user/', views.update_user, name='update_user'),
  path('witt_like/<int:pk>', views.witt_like, name='witt_like'),
  path('witt_show/<int:pk>', views.witt_show, name='witt_show'),
  path('delete_witt/<int:pk>', views.delete_witt, name='delete_witt'),
  path('search/', views.search, name='search'),
  path('search_user/', views.search_user, name='search_user'),
]
