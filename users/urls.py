# banking_system/users/urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users.views import RegisterUserView

urlpatterns = [
    path("login/", obtain_auth_token, name="api_token_auth"),
    path("register/", RegisterUserView.as_view(), name="api_register"),
]
