from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("buy/", views.purchase_ticket, name="buy_lotto"),
    path("results/", views.results_user, name="results_user"),
    path("results-admin/", views.admin_dashboard, name="results_admin"),
    path("draw/", views.draw_winning_numbers, name="admin_draw"),
]
