from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account

from transactions.models import Transaction
from transactions.serializers import (
    DepositSerializer,
    WithdrawSerializer,
    TransferSerializer,
    TransactionSerializer,
)
from transactions.services.transaction_service import TransactionService


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = Account.objects.get(id=serializer.validated_data["to_account_id"])
        txn = TransactionService.deposit(
            account, serializer.validated_data["amount"], request.user
        )
        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)


class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = Account.objects.get(id=serializer.validated_data["from_account_id"])
        txn = TransactionService.withdraw(
            account, serializer.validated_data["amount"], request.user
        )
        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_account = Account.objects.get(
            id=serializer.validated_data["from_account_id"]
        )
        to_account = Account.objects.get(id=serializer.validated_data["to_account_id"])
        txn = TransactionService.transfer(
            from_account, to_account, serializer.validated_data["amount"], request.user
        )
        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)


class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account_id = request.query_params.get("account_id")
        txns = Transaction.objects.all()
        if account_id:
            txns = txns.filter(from_account_id=account_id) | txns.filter(
                to_account_id=account_id
            )
        serializer = TransactionSerializer(txns, many=True)
        return Response(serializer.data)
