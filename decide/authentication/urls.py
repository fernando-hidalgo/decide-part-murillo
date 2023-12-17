from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import GetUserView, RegisterView, RegisterUserView, UserList, LoginUserView, LogoutView, LogoutUserView


urlpatterns = [
    path("login/", obtain_auth_token),
    path("logout/", LogoutView.as_view()),
    path("logoutuser/", LogoutUserView.as_view(), name="logout"),
    path("getuser/", GetUserView.as_view()),
    path("register/", RegisterView.as_view()),
    path("user/", UserList.as_view(), name="user-list"),
    path("registeruser/", RegisterUserView.as_view()),
    path("loginuser/", LoginUserView.as_view())
]
