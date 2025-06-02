from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# ----------------------
# USER MODEL
# ----------------------
class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
