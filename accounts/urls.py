from django.urls import path

from .views import login_api, logout_api, me_api, register_api

urlpatterns = [
    path("register/", register_api, name="api-register"),
    path("login/", login_api, name="api-login"),
    path("logout/", logout_api, name="api-logout"),
    path("me/", me_api, name="api-me"),
]
