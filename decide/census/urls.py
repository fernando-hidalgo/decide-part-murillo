from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.CensusCreate.as_view(), name="census_create"),
    path("<int:voting_id>/", views.CensusDetail.as_view(), name="census_detail"),
    path("import/", views.CensusImportView.as_view(), name="import_census"),
    path("yesno/", views.CensusYesNoCreate.as_view(), name="census_yesno_create"),
    path(
        "yesno/<int:voting_yesno_id>/",
        views.CensusYesNoDetail.as_view(),
        name="census_yesno_detail",
    ),
    path(
        "yesno/import/",
        views.CensusYesNoImportView.as_view(),
        name="import_census_yesno",
    ),
]
