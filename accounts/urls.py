# banking_system/accounts/urls.py
from django.urls import path
from accounts.views import AccountView

urlpatterns = [
    path("", AccountView.as_view(), name="accounts"),
]
