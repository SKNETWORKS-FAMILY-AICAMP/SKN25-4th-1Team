from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("smartcs.urls")),      
    path("accounts/", include("accounts.urls")),  # 로그인 추가
]


