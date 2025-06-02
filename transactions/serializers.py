from rest_framework import serializers
from decimal import Decimal
from transactions.models import Transaction


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    to_account_id = serializers.CharField(max_length=36)

    def validate(self, data):
        if data["amount"] <= 0:
            raise serializers.ValidationError("Deposit amount must be positive.")
        return data


class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    from_account_id = serializers.CharField(max_length=36)

    class Meta:
        fields = ["from_account_id", "amount"]

    def validate(self, data):
        if data["amount"] <= 0:
            raise serializers.ValidationError("Withdrawal amount must be positive.")
        return data


class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    to_account_id = serializers.CharField(max_length=36)
    from_account_id = serializers.CharField(max_length=36)

    def validate(self, data):
        if data["from_account_id"] == data["to_account_id"]:
            raise serializers.ValidationError("Cannot transfer to the same account.")
        if data["amount"] <= 0:
            raise serializers.ValidationError("Transfer amount must be positive.")
        return data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
