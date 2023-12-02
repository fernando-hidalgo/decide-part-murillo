from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.CensusCreate.as_view(), name="census_create"),
    path("bypreference/", views.CensusByPreferenceCreate.as_view(), name="census_by_preference_create"),
    path("<int:voting_id>/", views.CensusDetail.as_view(), name="census_detail"),
    path("bypreference/<int:voting_by_preference_id>/", views.CensusByPreferenceDetail.as_view(), name="census_by_preference_detail"),
    path("import/", views.CensusImportView.as_view(), name="import_census"),
    path("bypreference/import/", views.CensusImportView.as_view(), name="import_census_by_preference"),
]
