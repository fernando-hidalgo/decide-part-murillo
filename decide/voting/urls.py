from django.urls import path
from . import views


urlpatterns = [
    path("", views.VotingView.as_view(), name="voting"),
    path("<int:voting_id>/", views.VotingUpdate.as_view(), name="voting"),
    path("", views.VotingView.as_view(), name="voting"),
    path("<int:voting_id>/", views.VotingUpdate.as_view(), name="voting"),
    path("yesno/", views.VotingYNView.as_view(), name="votingyesno"),
    path(
        "yesno/<int:voting_yes_no_id>/",
        views.VotingYesNoUpdate.as_view(),
        name="votingyesno",
    ),
]
