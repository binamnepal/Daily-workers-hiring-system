from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.ServiceCategoryListView.as_view(), name="list"),
    path("<slug:slug>/", views.ServiceCategoryDetailView.as_view(), name="detail"),
]
