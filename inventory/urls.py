from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", __import__("django.contrib.auth.views", fromlist=["LogoutView"]).LogoutView.as_view(), name="logout"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("sales/new/", views.record_sale, name="record_sale"),
    path("sales/", views.sales_history, name="sales_history"),
]
