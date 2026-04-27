from django.urls import path

from frontend.webui import views


app_name = "webui"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/chat/", views.chat_api, name="chat-api"),
    path("api/session/device/", views.update_device, name="update-device"),
    path("api/session/reset/", views.reset_chat, name="reset-chat"),
]
