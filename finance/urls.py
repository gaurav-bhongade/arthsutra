from django.urls import path
from .views import loan_create, expense_create, income_create, finance_list, loan_emi_breakdown, department_create

urlpatterns = [
    path('loan/', loan_create, name='loan'),
    path('expense/', expense_create, name='expense'),
    path('income/', income_create, name='income'),
    path('department/', department_create, name='department'),
    path('list/', finance_list, name='finance_list'),
    path('loan/<int:loan_id>/breakdown/', loan_emi_breakdown, name='loan_emi_breakdown'),
]
