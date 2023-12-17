from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import GetUserView, RegisterView, RegisterUserView, UserList, LoginUserView, LogoutUserView


urlpatterns = [
    path("login/", obtain_auth_token),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("getuser/", GetUserView.as_view()),
    path("register/", RegisterView.as_view()),
    path("user/", UserList.as_view(), name="user-list"),
    path("registeruser/", RegisterUserView.as_view()),
    path("loginuser/", LoginUserView.as_view())
]
