from django.urls import path
from . import views


urlpatterns = [
    path("", views.VotingView.as_view(), name="voting"),
    path("<int:voting_id>/", views.VotingUpdate.as_view(), name="voting"),
    path("yesno/", views.VotingYNView.as_view(), name="votingyesno"),
    path(
        "yesno/<int:voting_yes_no_id>/",
        views.VotingYesNoUpdate.as_view(),
        name="votingyesno",
    ),
    path(
        "preference/", views.VotingByPreferenceView.as_view(), name="votingbypreference"
    ),
    path(
        "preference/<int:voting_by_preference_id>/",
        views.VotingByPreferenceUpdate.as_view(),
        name="votingbypreference",
    ),
    path("multichoice/", views.VotingMultiChoiceView.as_view(), name="votingmultichoice"),
    path(
        "multichoice/<int:voting_multichoice_id>/",
        views.VotingMultiChoiceUpdate.as_view(),
        name="votingmultichoice",
    ),
]
