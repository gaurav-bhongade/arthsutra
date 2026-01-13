from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Decorator to require admin role"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def expense_user_required(view_func):
    """Decorator to allow expense users and admins"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role not in ['ADMIN', 'EXPENSE_USER']:
            messages.error(request, 'Access denied. Insufficient privileges.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def income_user_required(view_func):
    """Decorator to allow income users and admins"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role not in ['ADMIN', 'INCOME_USER']:
            messages.error(request, 'Access denied. Insufficient privileges.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_or_expense_user_required(view_func):
    """Decorator to allow admins and expense users"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role not in ['ADMIN', 'EXPENSE_USER']:
            messages.error(request, 'Access denied. Insufficient privileges.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_or_income_user_required(view_func):
    """Decorator to allow admins and income users"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role not in ['ADMIN', 'INCOME_USER']:
            messages.error(request, 'Access denied. Insufficient privileges.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view