from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    
    path("signup/", UserSignupView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("profile/", userprofile.as_view()),
    path("changepass/", userchangepassword.as_view()),
    path("forgotPassword/", userforgotPasswordlinkSend.as_view()),
    path('map/',map.as_view()),
    path('userpost/', UserPostView.as_view()),
    path('allposts/',AllPostsView.as_view())
    
]
