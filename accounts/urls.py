from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.Login.as_view(),name='user_login'),
    path('signup/',views.SignUp.as_view(),name='user_signup'),
    path('logout/',views.Logout.as_view(),name='user_logout'),
    path('profile/',views.Profile.as_view(),name='profile'),
    path('change-password/',views.ChangePassword.as_view(),name='pass_change'),
    path('deposite/',views.DepositeView.as_view(),name='deposite'),
]