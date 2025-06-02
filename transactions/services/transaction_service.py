from decimal import Decimal
import uuid

from django.db import transaction as db_transaction

from accounts.models import Account
from accounts.rules.engine import get_account_rule_strategy
from transactions.models import Transaction


class TransactionService:
    """
    A class representing transaction services for handling deposit, withdrawal, and transfer operations.

    Attributes:
        None

    Methods:
        - deposit(to_account: Account, amount: Decimal, user) -> Transaction: Handles deposit operation by adding the specified amount to the account balance.
        - withdraw(from_account: Account, amount: Decimal, user) -> Transaction: Handles withdrawal operation by deducting the specified amount from the account balance.
        - transfer(from_account: Account, to_account: Account, amount: Decimal, user) -> Transaction: Handles transfer operation by deducting the amount from the sender's account and adding it to the receiver's account.
    """

    @staticmethod
    @db_transaction.atomic
    def deposit(to_account: Account, amount: Decimal, user) -> Transaction:
        strategy = get_account_rule_strategy(to_account)
        is_allowed, message = strategy.can_deposit(amount)
        if not is_allowed:
            raise ValueError(message)

        to_account.balance += amount
        to_account.save()

        txn = Transaction.objects.create(
            to_account=to_account, transaction_type="DEPOSIT", amount=amount
        )

        return txn

    @staticmethod
    @db_transaction.atomic
    def withdraw(from_account: Account, amount: Decimal, user) -> Transaction:
        strategy = get_account_rule_strategy(from_account)
        is_allowed, message = strategy.can_withdraw(amount)
        if not is_allowed:
            raise ValueError(message)

        fee = strategy.get_fee(amount)
        total = amount + fee
        if from_account.balance < total:
            raise ValueError("Insufficient balance including fees.")

        from_account.balance -= total
        from_account.save()

        txn = Transaction.objects.create(
            from_account=from_account, transaction_type="WITHDRAWAL", amount=amount
        )

        return txn

    @staticmethod
    @db_transaction.atomic
    def transfer(
        from_account: Account, to_account: Account, amount: Decimal, user
    ) -> Transaction:
        # Withdrawal rules on sender, deposit rules on receiver
        withdraw_strategy = get_account_rule_strategy(from_account)
        deposit_strategy = get_account_rule_strategy(to_account)

        is_withdraw_allowed, msg1 = withdraw_strategy.can_withdraw(amount)
        if not is_withdraw_allowed:
            raise ValueError(msg1)

        is_deposit_allowed, msg2 = deposit_strategy.can_deposit(amount)
        if not is_deposit_allowed:
            raise ValueError(msg2)

        fee = withdraw_strategy.get_fee(amount)
        total = amount + fee

        if from_account.balance < total:
            raise ValueError("Insufficient balance for transfer including fees.")

        from_account.balance -= total
        to_account.balance += amount

        from_account.save()
        to_account.save()

        txn = Transaction.objects.create(
            from_account=from_account,
            to_account=to_account,
            transaction_type="TRANSFER",
            amount=amount,
        )

        return txn
