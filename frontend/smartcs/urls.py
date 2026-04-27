from django.urls import include, path


urlpatterns = [
    path("", include("frontend.webui.urls")),
]
