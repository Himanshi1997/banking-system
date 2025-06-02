# banking_system/transactions/urls.py
from django.urls import path
from transactions.views import (
    DepositView,
    WithdrawView,
    TransferView,
    TransactionListView,
)

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("transfer/", TransferView.as_view(), name="transfer"),
    path("", TransactionListView.as_view(), name="transactions"),
]
