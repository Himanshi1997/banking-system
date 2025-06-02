# 0 0 1 */3 * docker-compose exec web python manage.py calculate_interest

from django.core.management.base import BaseCommand
from accounts.models import Account, InterestRecord, Transaction
from accounts.rules.engine import get_account_rule_strategy
from django.utils import timezone
import uuid


class Command(BaseCommand):
    help = "Apply quarterly interest to Regular Saving Accounts"

    def handle(self, *args, **options):
        now = timezone.now()
        accounts = Account.objects.filter(account_type="REGULAR", status="ACTIVE")

        for account in accounts:
            strategy = get_account_rule_strategy(account)
            interest = strategy.calculate_interest()

            if interest > 0:
                account.balance += interest
                account.save(update_fields=["balance"])

                # Create a transaction record for interest
                Transaction.objects.create(
                    to_account=account, transaction_type="DEPOSIT", amount=interest
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Applied ₹{interest:.2f} interest to Account ID {account.id}"
                    )
                )
