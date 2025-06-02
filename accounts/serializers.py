# banking_system/accounts/serializers.py
from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    account_type = serializers.ChoiceField(choices=Account.ACCOUNT_TYPE_CHOICES)

    class Meta:
        model = Account
        fields = [
            "id",
            "account_type",
            "balance",
            "status",
            "kyc_verified",
            "created_at",
        ]

    def validate_account_type(self, value):
        if value == "STUDENT":
            req = self.context.get("request")
            dob = req.user.date_of_birth
            if not dob:
                raise ValidationError("Date of birth required for Student Account.")
            today = date.today()
            age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )
            if age < 18 or age > 25:
                raise ValidationError("Age must be between 18-25 for Student Account.")

        return value
