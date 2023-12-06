from django.urls import path
from .views import VisualizerView, VisualizerViewPreference


urlpatterns = [
    path("<int:voting_id>/", VisualizerView.as_view()),
    path("preference/<int:voting_preference_id>/", VisualizerViewPreference.as_view()),
]
