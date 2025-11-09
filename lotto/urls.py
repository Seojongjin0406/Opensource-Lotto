from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("buy/", views.purchase_ticket, name="purchase_ticket"),
    path("results/", views.my_results, name="my_results"),
    path("results-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("draw/", views.draw_winning_numbers, name="draw_winning_numbers"),
]
