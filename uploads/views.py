from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UploadedFile
from .csv_processor import process_expense_csv, process_income_csv, process_department_csv
import os
from accounts.decorators import admin_required, admin_or_expense_user_required, admin_or_income_user_required

@login_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type')

        if not file or not file_type:
            messages.error(request, 'Please select a file and file type.')
            return redirect('upload')

        # Check user permissions based on file type
        user_role = request.user.role
        if file_type == 'DEPARTMENT' and user_role != 'ADMIN':
            messages.error(request, 'Only administrators can upload department data.')
            return redirect('upload')
        elif file_type == 'EXPENSE' and user_role not in ['ADMIN', 'EXPENSE_USER']:
            messages.error(request, 'Access denied. Insufficient privileges for expense uploads.')
            return redirect('upload')
        elif file_type == 'INCOME' and user_role not in ['ADMIN', 'INCOME_USER']:
            messages.error(request, 'Access denied. Insufficient privileges for income uploads.')
            return redirect('upload')

        # Validate file extension
        allowed_extensions = ['.csv', '.xlsx', '.xls']
        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension not in allowed_extensions:
            messages.error(request, 'Only CSV and Excel files are allowed.')
            return redirect('upload')

        # Save uploaded file record
        uploaded_file = UploadedFile.objects.create(
            user=request.user,
            file=file,
            file_type=file_type
        )

        try:
            file_path = uploaded_file.file.path

            if file_type == 'EXPENSE':
                processed_count = process_expense_csv(file_path, uploaded_file)
                messages.success(request, f'Successfully processed {processed_count} expense records.')
            elif file_type == 'INCOME':
                processed_count = process_income_csv(file_path, uploaded_file)
                messages.success(request, f'Successfully processed {processed_count} income records.')
            elif file_type == 'DEPARTMENT':
                processed_count = process_department_csv(file_path, uploaded_file)
                messages.success(request, f'Successfully processed {processed_count} department records.')

        except ValueError as e:
            messages.error(request, f'File format error: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            # Clean up the uploaded file record if processing failed
            uploaded_file.delete()

        return redirect('upload_history')

    return render(request, 'uploads/upload_new.html')

@login_required
def upload_history(request):
    uploads = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'uploads/history_new.html', {'uploads': uploads})
