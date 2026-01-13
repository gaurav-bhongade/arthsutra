print("Starting CSV test...")
import os
import django

print("Setting up Django...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arthsutra.settings')
django.setup()

print("Importing modules...")
from uploads.csv_processor import process_department_csv
from uploads.models import UploadedFile
from django.contrib.auth.models import User

print("Creating test user...")
# Create a test user if not exists
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
print(f"User created: {created}, User: {user}")

# Create a test uploaded file record
print("Creating uploaded file record...")
uploaded_file = UploadedFile.objects.create(
    user=user,
    file='sample_department_data.csv',
    file_type='DEPARTMENT'
)
print(f"Uploaded file created: {uploaded_file}")

# Test processing with absolute path
file_path = os.path.join(os.getcwd(), 'uploads', 'sample_department_data.csv')
print(f"Testing with file path: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

try:
    print("Processing CSV...")
    count = process_department_csv(file_path, uploaded_file)
    print(f'Successfully processed {count} department records')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()