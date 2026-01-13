from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

class Expense(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class Income(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class Loan(models.Model):
    loan_name = models.CharField(max_length=100)
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.FloatField()
    tenure_months = models.IntegerField()
    emi = models.DecimalField(max_digits=10, decimal_places=2)
