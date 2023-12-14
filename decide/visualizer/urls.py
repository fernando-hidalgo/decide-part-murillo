from django.urls import path
from .views import VisualizerView, VisualizerViewPreference, VisualizerViewYesNo


urlpatterns = [
    path("<int:voting_id>/", VisualizerView.as_view()),
    path("preference/<int:voting_preference_id>/", VisualizerViewPreference.as_view()),
    path("yesno/<int:voting_yesno_id>/", VisualizerViewYesNo.as_view()),
]
