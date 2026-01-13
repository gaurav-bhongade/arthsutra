from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Loan, Expense, Income, Department
from .services import calculate_emi, calculate_emi_breakdown
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
from accounts.decorators import admin_required, admin_or_expense_user_required, admin_or_income_user_required

@admin_required
def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Department.objects.create(name=name)
            messages.success(request, f'Department "{name}" created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Department name cannot be empty.')

    departments = Department.objects.all().order_by('name')
    context = {
        'departments': departments,
    }

    return render(request, 'finance/department_new.html', context)

@admin_required
def loan_create(request):
    if request.method == 'POST':
        try:
            principal = float(request.POST['principal'])
            rate = float(request.POST['rate'])
            months = int(request.POST['months'])

            emi = calculate_emi(principal, rate, months)

            Loan.objects.create(
                loan_name=request.POST['name'],
                principal=principal,
                interest_rate=rate,
                tenure_months=months,
                emi=emi
            )
            messages.success(request, 'Loan created successfully!')
            return redirect('dashboard')
        except ValueError:
            messages.error(request, 'Please enter valid numeric values.')

    return render(request, 'finance/loan_new.html')

@admin_or_expense_user_required
def expense_create(request):
    if request.method == 'POST':
        try:
            department_id = request.POST['department']
            expense_type = request.POST['expense_type']
            amount = float(request.POST['amount'])
            date = request.POST['date']

            Expense.objects.create(
                department_id=department_id,
                expense_type=expense_type,
                amount=amount,
                date=date
            )
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')
        except ValueError:
            messages.error(request, 'Please enter valid data.')

    departments = Department.objects.all()
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    today = timezone.now().date()

    context = {
        'departments': departments,
        'total_expenses': total_expenses,
        'today': today,
    }

    return render(request, 'finance/expense_new.html', context)

@admin_or_income_user_required
def income_create(request):
    if request.method == 'POST':
        try:
            department_id = request.POST['department']
            service_type = request.POST['service_type']
            amount = float(request.POST['amount'])
            date = request.POST['date']

            Income.objects.create(
                department_id=department_id,
                service_type=service_type,
                amount=amount,
                date=date
            )
            messages.success(request, 'Income added successfully!')
            return redirect('dashboard')
        except ValueError:
            messages.error(request, 'Please enter valid data.')

    departments = Department.objects.all()
    total_income = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    today = timezone.now().date()

    context = {
        'departments': departments,
        'total_income': total_income,
        'today': today,
    }

    return render(request, 'finance/income_new.html', context)

@login_required
def finance_list(request):
    user_role = request.user.role

    # Filter data based on user role
    if user_role == 'ADMIN':
        expenses = Expense.objects.select_related('department').order_by('-date')
        incomes = Income.objects.select_related('department').order_by('-date')
        loans = Loan.objects.all()
    elif user_role == 'EXPENSE_USER':
        expenses = Expense.objects.select_related('department').order_by('-date')
        incomes = Income.objects.none()  # Empty queryset
        loans = Loan.objects.none()  # Empty queryset
    elif user_role == 'INCOME_USER':
        expenses = Expense.objects.none()  # Empty queryset
        incomes = Income.objects.select_related('department').order_by('-date')
        loans = Loan.objects.none()  # Empty queryset
    else:
        # Fallback for any other roles
        expenses = Expense.objects.none()
        incomes = Income.objects.none()
        loans = Loan.objects.none()

    # Calculate totals based on visible data
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_loans = loans.aggregate(Sum('principal'))['principal__sum'] or 0

    context = {
        'expenses': expenses,
        'incomes': incomes,
        'loans': loans,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'total_loans': total_loans,
        'user_role': user_role,
    }

    return render(request, 'finance/list.html', context)

@login_required
def loan_emi_breakdown(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    emi_breakdown = calculate_emi_breakdown(
        float(loan.principal),
        loan.interest_rate,
        loan.tenure_months
    )

    context = {
        'loan': loan,
        'emi_breakdown': emi_breakdown,
        'total_principal': loan.principal,
        'total_interest': sum(item['interest_payment'] for item in emi_breakdown),
        'total_amount': sum(item['emi'] for item in emi_breakdown),
    }

    return render(request, 'finance/loan_breakdown.html', context)
