from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/customer/", views.RegisterCustomerView.as_view(), name="register-customer"),
    path("register/worker/", views.RegisterWorkerView.as_view(), name="register-worker"),
    path("me/", views.MeView.as_view(), name="me"),
    path("me/location/", views.UpdateLocationView.as_view(), name="update-location"),
]
