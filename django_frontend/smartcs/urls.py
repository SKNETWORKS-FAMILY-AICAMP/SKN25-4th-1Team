from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("chat/", views.chat_api, name="chat_api"),
    path("chat/reset/", views.reset_chat, name="reset_chat"),
    path("device/", views.update_device, name="update_device"),
    path("faq/", views.faq_browser, name="faq_browser"),
    path("search/", views.search, name="search"),
    path("service-centers/", views.service_centers, name="service_centers"),
]
