from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, RegisterView, RegisterUserView, LoginView, LoginUserView


urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("getuser/", GetUserView.as_view()),
    path("register/", RegisterView.as_view()),
    path("registeruser/", RegisterUserView.as_view()),
    path("loginuser/", LoginUserView.as_view())
]
