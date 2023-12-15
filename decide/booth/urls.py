from django.urls import path
from .views import BoothPreferenceView, BoothView, BoothYesNoView


urlpatterns = [
    path("<int:voting_id>/", BoothView.as_view()),
    path("preference/<int:voting_id>/", BoothPreferenceView.as_view()),
    path("yesno/<int:voting_id>/", BoothYesNoView.as_view()),
]
