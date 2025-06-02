import uuid

from django.db import models
from users.models import User


# Create your models here.
# ----------------------
# ACCOUNT BASE MODEL
# ----------------------
class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ("ZERO", "Zero Balance"),
        ("STUDENT", "Student"),
        ("REGULAR", "Regular Saving"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("SUSPENDED", "Suspended"),
        ("CLOSED", "Closed"),
    ]

    id = models.CharField(
        max_length=36, primary_key=True, default=uuid.uuid4
    )  # UUID or custom ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_type = models.CharField(
        max_length=100, choices=ACCOUNT_TYPE_CHOICES, default="ZERO"
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    kyc_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"
