from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.db.models import Q


class AccountRuleStrategy(ABC):
    """
    AccountRuleStrategy is the base interface for rule enforcement
    """

    def __init__(self, account):
        self.account = account
        self.now = timezone.now()

    @abstractmethod
    def can_deposit(self, amount: Decimal) -> (bool, str):
        pass

    @abstractmethod
    def can_withdraw(self, amount: Decimal) -> (bool, str):
        pass

    @abstractmethod
    def get_fee(self, amount: Decimal) -> Decimal:
        pass

    def calculate_interest(self) -> Decimal:
        """
        Calculate interest for the account based on its type.
        This method can be overridden by specific account rules if needed.
        """
        return Decimal("0")


# ----------------------
# ZERO BALANCE ACCOUNT RULES
# ----------------------
class ZeroBalanceRule(AccountRuleStrategy):
    def can_deposit(self, amount):
        return True, ""

    def can_withdraw(self, amount):

        month_start = self.now.replace(day=1)
        withdrawals = Transaction.objects.filter(
            from_account=self.account,
            transaction_type="WITHDRAWAL",
            created_at__gte=month_start,
        ).count()
        if withdrawals >= 4:
            return False, "Withdrawal limit exceeded for Zero Balance Account."
        return True, ""

    def get_fee(self, amount):
        return Decimal("0")


# ----------------------
# STUDENT ACCOUNT RULES
# ----------------------
class StudentAccountRule(AccountRuleStrategy):
    def can_deposit(self, amount):
        from transactions.models import Transaction

        month_start = self.now.replace(day=1)
        total_monthly_deposits = Transaction.objects.filter(
            to_account=self.account,
            transaction_type="DEPOSIT",
            created_at__gte=month_start,
        ).aggregate(models.Sum("amount"))["amount__sum"] or Decimal("0")

        if total_monthly_deposits + amount > Decimal("10000"):
            return False, "Monthly deposit limit of ₹10,000 exceeded."
        return True, ""

    def can_withdraw(self, amount):
        from transactions.models import Transaction

        if self.account.balance - amount < Decimal("1000"):
            return False, "Minimum balance ₹1,000 required."

        month_start = self.now.replace(day=1)
        withdrawals = Transaction.objects.filter(
            from_account=self.account,
            transaction_type="WITHDRAWAL",
            created_at__gte=month_start,
        ).count()
        if withdrawals >= 4:
            return False, "Withdrawal limit exceeded for Student Account."

        return True, ""

    def get_fee(self, amount):
        return Decimal("0")


# ----------------------
# REGULAR SAVING ACCOUNT RULES
# ----------------------
class RegularSavingRule(AccountRuleStrategy):
    def can_deposit(self, amount):
        from transactions.models import Transaction

        month_start = self.now.replace(day=1)
        total_monthly_deposits = Transaction.objects.filter(
            to_account=self.account,
            transaction_type="DEPOSIT",
            created_at__gte=month_start,
        ).aggregate(models.Sum("amount"))["amount__sum"] or Decimal("0")

        if (
            total_monthly_deposits + amount > Decimal("50000")
            and not self.account.kyc_verified
        ):
            return False, "KYC verification required for deposits exceeding ₹50,000."
        return True, ""

    def can_withdraw(self, amount):
        from transactions.models import Transaction

        # Check average balance for last 90 days

        ninety_days_ago = self.now - timedelta(days=90)
        txn_snapshots = Transaction.objects.filter(
            (Q(from_account=self.account) | Q(to_account=self.account))
            & Q(created_at__gte=ninety_days_ago)
        ).order_by("created_at")

        # Approximate method: sum the balance at each transaction point, assume constant otherwise
        total_balance = Decimal("0")
        last_balance = self.account.balance
        if txn_snapshots.exists():
            timestamps = list(txn_snapshots.values_list("created_at", flat=True))
            timestamps = [ninety_days_ago] + timestamps + [self.now]
            durations = [
                (timestamps[i + 1] - timestamps[i]).total_seconds() / 86400  # in days
                for i in range(len(timestamps) - 1)
            ]
            for days in durations:
                total_balance += last_balance * Decimal(str(days))
            average_balance = total_balance / Decimal("90")
        else:
            average_balance = self.account.balance  # fallback to current

        if average_balance < Decimal("5000"):
            return False, "Minimum 90-day average balance ₹5,000 required."

        return True, ""

    def get_fee(self, amount):
        from transactions.models import Transaction

        month_start = self.now.replace(day=1)
        withdrawals = Transaction.objects.filter(
            from_account=self.account,
            transaction_type="WITHDRAWAL",
            created_at__gte=month_start,
        ).count()

        return Decimal("5") * (withdrawals - 10) if withdrawals > 10 else Decimal("0")

    def calculate_interest(self) -> Decimal:
        # Interest is calculated on 90-day average balance
        from transactions.models import Transaction

        ninety_days_ago = self.now - timedelta(days=90)
        txn_snapshots = Transaction.objects.filter(
            (Q(from_account=self.account) | Q(to_account=self.account))
            & Q(created_at__gte=ninety_days_ago)
        ).order_by("created_at")

        total_balance = Decimal("0")
        last_balance = self.account.balance
        if txn_snapshots.exists():
            timestamps = list(txn_snapshots.values_list("created_at", flat=True))
            timestamps = [ninety_days_ago] + timestamps + [self.now]
            durations = [
                (timestamps[i + 1] - timestamps[i]).total_seconds() / 86400
                for i in range(len(timestamps) - 1)
            ]
            for days in durations:
                total_balance += last_balance * Decimal(str(days))
            average_balance = total_balance / Decimal("90")
        else:
            average_balance = self.account.balance

        interest_rate = Decimal("0.01")  # 1% quarterly interest
        return (average_balance * interest_rate).quantize(Decimal("0.01"))


# ----------------------
# FACTORY FOR STRATEGY
# ----------------------
def get_account_rule_strategy(account):
    if account.account_type == "ZERO":
        return ZeroBalanceRule(account)
    elif account.account_type == "STUDENT":
        return StudentAccountRule(account)
    elif account.account_type == "REGULAR":
        return RegularSavingRule(account)
    else:
        raise ValueError("Invalid account type")
