from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .decorators import admin_required
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserCreationFormWithRole(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@admin_required
def user_list(request):
    users = User.objects.all().order_by('username')

    # Calculate statistics
    total_users = users.count()
    admin_count = users.filter(role='ADMIN').count()
    expense_count = users.filter(role='EXPENSE_USER').count()
    income_count = users.filter(role='INCOME_USER').count()

    context = {
        'users': users,
        'total_users': total_users,
        'admin_count': admin_count,
        'expense_count': expense_count,
        'income_count': income_count,
    }

    return render(request, 'accounts/user_list.html', context)

from django.contrib.auth import get_user_model

User = get_user_model()

@admin_required
def user_create(request):
    if request.method == 'POST':
        form = UserCreationFormWithRole(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('user_list')
        else:
            print("FORM ERRORS:", form.errors)  # 🔴 ADD THIS
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationFormWithRole()

    # ---- ADD COUNTS HERE ----
    total_users = User.objects.count()
    admin_count = User.objects.filter(is_staff=True).count()
    expense_count = User.objects.filter(role='expense').count()
    income_count = User.objects.filter(role='income').count()

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': 'Create User',
        'total_users': total_users,
        'admin_count': admin_count,
        'expense_count': expense_count,
        'income_count': income_count,
    })

@admin_required
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserCreationFormWithRole(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} updated successfully.')
            return redirect('user_list')
    else:
        form = UserCreationFormWithRole(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Update User'})


from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_superuser and request.user.role != 'ADMIN':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)
    return wrapper




@admin_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_list')

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully.")
        return redirect('user_list')

    # GET request → show confirmation page
    return render(request, 'accounts/user_confirm_delete.html', {
        'user': user
    })



