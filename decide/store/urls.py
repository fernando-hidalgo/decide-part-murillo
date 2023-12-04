from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path("yesno", views.StoreYNView.as_view(), name="storeyesno"),
    path(
        "preference/", views.StoreByPreferenceView.as_view(), name="storebypreference"
    ),
]
