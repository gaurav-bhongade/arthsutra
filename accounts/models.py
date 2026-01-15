from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('EXPENSE_USER', 'Expense User'),
        ('INCOME_USER', 'Income User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ADMIN')
