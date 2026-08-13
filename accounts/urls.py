from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_chooser, name="register"),
    path("register/customer/", views.register_customer, name="register_customer"),
    path("register/worker/", views.register_worker, name="register_worker"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path(
        "dashboard/customer/",
        views.customer_dashboard,
        name="customer_dashboard",
    ),

    path(
        "dashboard/worker/",
        views.worker_dashboard,
        name="worker_dashboard",
    ),

    path("location/", views.update_location, name="update_location"),
]