#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('f:\\Projects\\Arthsutra\\arthsutra')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arthsutra.settings')
django.setup()

from accounts.models import User

def create_test_users():
    print('Existing users:')
    for u in User.objects.all():
        print(f'{u.username}: {u.role}')

    print('\nCreating test users...')

    # Create admin user
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='ADMIN')
        print('Created admin user')

    # Create expense user
    if not User.objects.filter(username='expense_user').exists():
        User.objects.create_user('expense_user', 'expense@example.com', 'pass123', role='EXPENSE_USER')
        print('Created expense user')

    # Create income user
    if not User.objects.filter(username='income_user').exists():
        User.objects.create_user('income_user', 'income@example.com', 'pass123', role='INCOME_USER')
        print('Created income user')

    print('Test users created successfully!')

if __name__ == '__main__':
    create_test_users()