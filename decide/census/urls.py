from django.urls import path
from . import views


urlpatterns = [
    path("", views.CensusCreate.as_view(), name="census_create"),
    path(
        "bypreference/",
        views.CensusByPreferenceCreate.as_view(),
        name="census_by_preference_create",
    ),
    path("yesno/", views.CensusYesNoCreate.as_view(), name="census_yesno_create"),
    path("multichoice/", views.CensusMultiChoiceCreate.as_view(), name="census_multichoice_create"),
    path("<int:voting_id>/", views.CensusDetail.as_view(), name="census_detail"),
    path(
        "bypreference/<int:voting_id>/",
        views.CensusByPreferenceDetail.as_view(),
        name="census_by_preference_detail",
    ),
    path(
        "yesno/<int:voting_id>/",
        views.CensusYesNoDetail.as_view(),
        name="census_yesno_detail",
    ),
    path(
        "multichoice/<int:voting_id>/",
        views.CensusMultiChoiceDetail.as_view(),
        name="census_multichoice_detail",
    ),
    path("import/", views.CensusImportView.as_view(), name="import_census"),
    path("admin/", views.CensusAdminView.as_view(), name="admin_census"),
    path("api/census/", views.CensusListCreateAPIView.as_view(), name="api_census"),
    path("create/", views.CensusCreateView.as_view(), name="census-create"),
    path(
        "bypreference/import/",
        views.CensusImportView.as_view(),
        name="import_census_by_preference",
    ),
    path(
        "yesno/import/",
        views.CensusYesNoImportView.as_view(),
        name="import_census_yesno",
    ),
    path(
        "multichoice/import/",
        views.CensusMultiChoiceImportView.as_view(),
        name="import_census_multichoice",
    ),
]
