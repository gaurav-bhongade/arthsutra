from rest_framework import serializers
from .models import Loan, Expense, Income

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
