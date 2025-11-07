from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                       # 홈
    path('buy/', views.buy_lotto, name='buy_lotto'),         # 사용자 구매
    path('results/', views.results_user, name='results_user'),
    path('admin-draw/', views.admin_draw, name='admin_draw'),
    path('results-admin/', views.results_admin, name='results_admin'),
]
