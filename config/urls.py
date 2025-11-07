from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lotto.urls')),  # ← lotto 앱 라우팅 연결
]
