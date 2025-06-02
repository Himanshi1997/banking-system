# banking_system/accounts/tests/test_accounts.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta

User = get_user_model()


class AccountCreationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="student1",
            password="testpass",
            date_of_birth=date.today() - timedelta(days=365 * 20),  # 20 years old
        )
        self.client.force_authenticate(user=self.user)

    def test_create_student_account_success(self):
        response = self.client.post("/api/create-account/", {"account_type": "STUDENT"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["account_type"], "STUDENT")

    def test_student_account_rejects_age_under_18(self):
        self.user.date_of_birth = date.today() - timedelta(days=365 * 17)
        self.user.save()
        response = self.client.post("/api/create-account/", {"account_type": "STUDENT"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Age must be between 18-25", str(response.data))

    def test_student_account_rejects_age_above_25(self):
        self.user.date_of_birth = date.today() - timedelta(days=365 * 26)
        self.user.save()
        response = self.client.post("/api/create-account/", {"account_type": "STUDENT"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Age must be between 18-25", str(response.data))

    def test_regular_account_success(self):
        response = self.client.post("/api/create-account/", {"account_type": "REGULAR"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["account_type"], "REGULAR")
