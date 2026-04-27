from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("chat/", views.chat_api, name="chat"),
]
