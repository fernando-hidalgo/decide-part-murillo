from django.urls import path
from .views import BoothPreferenceView, BoothView, BoothYesNoView, BoothMultiChoiceView


urlpatterns = [
    path("<int:voting_id>/", BoothView.as_view()),
    path("preference/<int:voting_id>/", BoothPreferenceView.as_view()),
    path("yesno/<int:voting_id>/", BoothYesNoView.as_view()),
    path("multichoice/<int:voting_id>/", BoothMultiChoiceView.as_view()),
]
