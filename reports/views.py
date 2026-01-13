from django.shortcuts import render
from django.db.models import Sum, Count
from finance.models import Income, Expense, Department, Loan
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, date
import json
from accounts.decorators import admin_required

@login_required
def dashboard(request):
    user_role = request.user.role

    # Filter data based on user role
    if user_role == 'ADMIN':
        # Show all data
        income_queryset = Income.objects
        expense_queryset = Expense.objects
        loan_queryset = Loan.objects
    elif user_role == 'EXPENSE_USER':
        # Show only expense-related data
        income_queryset = Income.objects.none()
        expense_queryset = Expense.objects
        loan_queryset = Loan.objects.none()
    elif user_role == 'INCOME_USER':
        # Show only income-related data
        income_queryset = Income.objects
        expense_queryset = Expense.objects.none()
        loan_queryset = Loan.objects.none()
    else:
        # Fallback
        income_queryset = Income.objects.none()
        expense_queryset = Expense.objects.none()
        loan_queryset = Loan.objects.none()

    # Overall totals
    total_income = income_queryset.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expense_queryset.aggregate(Sum('amount'))['amount__sum'] or 0
    total_profit = total_income - total_expense

    # Monthly data (last 6 months)
    today = timezone.now().date()
    months_data = []
    for i in range(5, -1, -1):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        monthly_income = income_queryset.filter(date__range=[month_start, month_end]).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_expense = expense_queryset.filter(date__range=[month_start, month_end]).aggregate(Sum('amount'))['amount__sum'] or 0

        months_data.append({
            'month': month_start.strftime('%b %Y'),
            'income': float(monthly_income),
            'expense': float(monthly_expense),
            'profit': float(monthly_income - monthly_expense)
        })

    # Department-wise summary (filtered by user role)
    if user_role == 'ADMIN':
        departments = list(Department.objects.annotate(
            total_income=Sum('income__amount'),
            total_expense=Sum('expense__amount'),
            income_count=Count('income'),
            expense_count=Count('expense')
        ).values('name', 'total_income', 'total_expense', 'income_count', 'expense_count'))
    elif user_role == 'EXPENSE_USER':
        departments = list(Department.objects.annotate(
            total_income=Sum('income__amount'),
            total_expense=Sum('expense__amount'),
            income_count=Count('income'),
            expense_count=Count('expense')
        ).values('name', 'total_income', 'total_expense', 'income_count', 'expense_count'))
        # For expense users, show departments with expenses
        departments = [d for d in departments if d['total_expense'] and d['total_expense'] > 0]
    elif user_role == 'INCOME_USER':
        departments = list(Department.objects.annotate(
            total_income=Sum('income__amount'),
            total_expense=Sum('expense__amount'),
            income_count=Count('income'),
            expense_count=Count('expense')
        ).values('name', 'total_income', 'total_expense', 'income_count', 'expense_count'))
        # For income users, show departments with income
        departments = [d for d in departments if d['total_income'] and d['total_income'] > 0]

    # Convert to JSON-serializable format
    for dept in departments:
        dept['total_income'] = float(dept['total_income'] or 0)
        dept['total_expense'] = float(dept['total_expense'] or 0)

    # Recent transactions (filtered by role)
    recent_expenses = expense_queryset.select_related('department').order_by('-date')[:10]
    recent_income = income_queryset.select_related('department').order_by('-date')[:10]

    # Loan summary (only for admins)
    if user_role == 'ADMIN':
        total_loans = loan_queryset.aggregate(Sum('principal'))['principal__sum'] or 0
        active_loans = loan_queryset.count()
    else:
        total_loans = 0
        active_loans = 0

    context = {
        'total_income': total_income,
        'total_expenses': total_expense,
        'net_profit': total_profit,
        'monthly_labels': json.dumps([item['month'] for item in months_data]),
        'monthly_income': json.dumps([item['income'] for item in months_data]),
        'monthly_expenses': json.dumps([item['expense'] for item in months_data]),
        'department_labels': json.dumps([dept['name'] for dept in departments]),
        'department_data': json.dumps([dept['total_income'] for dept in departments]),
        'recent_expenses': recent_expenses,
        'recent_income': recent_income,
        'total_loans': total_loans,
        'active_loans': active_loans,
        'user_role': user_role,
    }

    return render(request, 'dashboard/dashboard_new.html', context)

@login_required
def reports_view(request):
    user_role = request.user.role

    # Filter data based on user role
    if user_role == 'ADMIN':
        income_queryset = Income.objects
        expense_queryset = Expense.objects
    elif user_role == 'EXPENSE_USER':
        income_queryset = Income.objects.none()
        expense_queryset = Expense.objects
    elif user_role == 'INCOME_USER':
        income_queryset = Income.objects
        expense_queryset = Expense.objects.none()
    else:
        income_queryset = Income.objects.none()
        expense_queryset = Expense.objects.none()

    # Generate various reports
    department_report = Department.objects.annotate(
        income_total=Sum('income__amount'),
        expense_total=Sum('expense__amount'),
        transaction_count=Count('income') + Count('expense')
    ).values('name', 'income_total', 'expense_total', 'transaction_count')

    # Convert to list and calculate net profit
    department_report = list(department_report)
    for dept in department_report:
        income = dept['income_total'] or 0
        expense = dept['expense_total'] or 0
        dept['net_profit'] = income - expense

    # Filter department report based on user role
    if user_role == 'EXPENSE_USER':
        department_report = [d for d in department_report if d['expense_total'] and d['expense_total'] > 0]
    elif user_role == 'INCOME_USER':
        department_report = [d for d in department_report if d['income_total'] and d['income_total'] > 0]

    # Monthly trends - Last 12 months
    monthly_trends = []
    today = timezone.now().date()

    for i in range(11, -1, -1):  # From 11 months ago to current month
        # Calculate the target month
        year = today.year
        month = today.month - i

        # Adjust for year wraparound
        while month <= 0:
            month += 12
            year -= 1

        month_start = date(year, month, 1)

        # Calculate month end
        if month == 12:
            month_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(year, month + 1, 1) - timedelta(days=1)

        income = income_queryset.filter(date__range=[month_start, month_end]).aggregate(Sum('amount'))['amount__sum'] or 0
        expense = expense_queryset.filter(date__range=[month_start, month_end]).aggregate(Sum('amount'))['amount__sum'] or 0

        monthly_trends.append({
            'month': month_start.strftime('%B %Y'),
            'income': float(income),
            'expense': float(expense),
            'profit': float(income - expense)
        })

    context = {
        'department_report': department_report,
        'monthly_trends': monthly_trends,
        'monthly_trends_json': json.dumps(monthly_trends),
        'user_role': user_role,
    }

    return render(request, 'reports/reports_new.html', context)
