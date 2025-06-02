from django.shortcuts import render

# Create your views here.
# banking_system/accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        account_type = serializer.validated_data["account_type"]

        # Age check for Student Account

        account = Account.objects.create(
            user=request.user, account_type=account_type, balance=0.0  # Start with zero
        )
        return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        accounts = Account.objects.filter(user=request.user.id)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
