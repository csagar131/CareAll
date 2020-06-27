from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from accounts.views import ElderUserCreate,YoungerUserCreate,DisplayProfileView,EditProfileView,UserDashboardView,AddFundView
from caremain.views import AcceptRejectRequestView


urlpatterns = [
    path('signup/elder',ElderUserCreate.as_view(),name = 'signup_elder'),
    path('signup/younger',YoungerUserCreate.as_view(),name = 'signup_younger'),
    path('login',LoginView.as_view(template_name='login.html'),name = 'login'),
    path('logout',LogoutView.as_view(),name = 'logout'),
    path('profile/<slug:slug>',DisplayProfileView.as_view(),name = 'profile'),
    path('profile/update/<slug:slug>',EditProfileView.as_view(),name = 'editprofile'),
    path('dashboard',UserDashboardView.as_view(),name = 'dashboard'),
    path('dashboard/<str:str>/<slug:slug>',AcceptRejectRequestView.as_view(),name = 'ar_request'),
    path('<slug:slug>/addfund',AddFundView.as_view(),name = 'addfund'),
]