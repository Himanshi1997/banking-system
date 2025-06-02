import uuid
from django.db import models
from accounts.models import Account


# Create your models here.
# ----------------------
# TRANSACTION MODEL
# ----------------------
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
        ("TRANSFER", "Transfer"),
    ]

    TRANSACTION_STATUS = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="outgoing_transactions",
        null=True,
        blank=True,
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="incoming_transactions",
        null=True,
        blank=True,
    )

    id = models.CharField(
        max_length=36, primary_key=True, default=uuid.uuid4
    )  # UUID or custom ID
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["from_account"]),
            models.Index(fields=["to_account"]),
            models.Index(fields=["created_at"]),
        ]
