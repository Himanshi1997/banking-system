# banking_system/transactions/tests/test_transactions.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Account
from transactions.services.transaction_service import TransactionService
from decimal import Decimal

User = get_user_model()


class TransactionServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", password="pass", date_of_birth="2000-01-01"
        )
        self.acc1 = Account.objects.create(
            user=self.user, account_type="REGULAR", balance=Decimal("10000.00")
        )
        self.acc2 = Account.objects.create(
            user=self.user, account_type="REGULAR", balance=Decimal("5000.00")
        )

    def test_deposit_success(self):
        txn = TransactionService.deposit(self.acc1, Decimal("1000"), self.user)
        self.acc1.refresh_from_db()
        self.assertEqual(txn.amount, Decimal("1000"))
        self.assertEqual(self.acc1.balance, Decimal("11000"))

    def test_withdraw_success(self):
        txn = TransactionService.withdraw(self.acc1, Decimal("1000"), self.user)
        self.acc1.refresh_from_db()
        self.assertEqual(txn.amount, Decimal("1000"))
        self.assertEqual(
            self.acc1.balance, Decimal("9000")
        )  # no fee for first 10 withdrawals

    def test_transfer_success(self):
        txn = TransactionService.transfer(
            self.acc1, self.acc2, Decimal("2000"), self.user
        )
        self.acc1.refresh_from_db()
        self.acc2.refresh_from_db()
        self.assertEqual(txn.amount, Decimal("2000"))
        self.assertEqual(self.acc1.balance, Decimal("8000"))
        self.assertEqual(self.acc2.balance, Decimal("7000"))

    def test_overdraft_should_fail(self):
        with self.assertRaises(ValueError):
            TransactionService.withdraw(self.acc2, Decimal("6000"), self.user)

    def test_reverse_transaction(self):
        txn = TransactionService.deposit(self.acc1, Decimal("1500"), self.user)
        self.acc1.refresh_from_db()
        balance_after = self.acc1.balance
        reversed_txn = TransactionService.reverse(txn.id, self.user)
        self.acc1.refresh_from_db()
        self.assertTrue(reversed_txn.reversed)
        self.assertEqual(self.acc1.balance, balance_after - Decimal("1500"))
