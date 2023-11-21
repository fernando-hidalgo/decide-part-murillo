from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.CensusCreate.as_view(), name="census_create"),
    path("<int:voting_id>/", views.CensusDetail.as_view(), name="census_detail"),
    path("import/", views.CensusImportView.as_view(), name="import_census"),
    path("admin/", views.CensusAdminView.as_view(), name="admin_census"),
    path("api/census/", views.CensusListCreateAPIView.as_view(), name="api_census"),
    path("create/", views.CensusCreateView.as_view(), name="census-create"),
]
