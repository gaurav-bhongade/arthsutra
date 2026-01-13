# ArthSutra - Healthcare Finance Management System

A comprehensive Django-based web application for managing healthcare financial operations, including income tracking, expense management, loan calculations, and detailed reporting.

## Features

### 🔐 Authentication & User Management
- Custom user roles (Admin, Healthcare Admin)
- Secure login/logout system
- Role-based access control

### 💰 Financial Management
- **Income Tracking**: Record revenue from various healthcare services
- **Expense Management**: Track departmental expenses
- **Loan Management**: Calculate EMIs for healthcare equipment loans
- **Department-wise Organization**: Categorize finances by medical departments

### 📊 Dashboard & Analytics
- Real-time financial overview
- Interactive charts (monthly trends, department performance)
- Key performance indicators (KPIs)
- Recent transactions view

### 📈 Reports & Insights
- Department-wise financial reports
- 12-month trend analysis
- Profit/loss analysis
- Exportable reports

### 📤 Data Import/Export
- CSV/Excel file upload support
- Bulk data processing for expenses, income, and departments
- Upload history tracking
- Error handling and validation

### 🎨 Modern UI/UX
- Bootstrap 5 responsive design
- Interactive charts with Chart.js
- Mobile-friendly interface
- Intuitive navigation

## Technology Stack

- **Backend**: Django 6.0.1
- **Database**: MySQL (with SQLite fallback)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts**: Chart.js
- **File Processing**: Pandas
- **Authentication**: Django's built-in auth system

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server (or use SQLite for development)
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd arthsutra
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Load Sample Data
```bash
python manage.py shell
```
```python
from finance.models import Department
from accounts.models import User

# Create sample departments
departments = ['Cardiology', 'Radiology', 'Pharmacy', 'Emergency', 'Surgery', 'Pediatrics']
for dept_name in departments:
    Department.objects.get_or_create(name=dept_name)

# Create sample user
User.objects.create_user(
    username='health_admin',
    email='admin@hospital.com',
    password='admin123',
    role='HEALTHCARE_ADMIN'
)
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Usage Guide

### Login Credentials
- **Username**: health_admin
- **Password**: admin123

### Key Features Overview

#### Dashboard
- View overall financial health
- Monitor monthly trends
- Track recent transactions
- Access quick action buttons

#### Finance Management
- **Add Expenses**: Record departmental expenses with categories
- **Add Income**: Track revenue from healthcare services
- **Manage Loans**: Calculate EMIs for equipment financing
- **View All Records**: Comprehensive financial overview

#### Reports
- Department-wise performance analysis
- 12-month financial trends
- Profit/loss tracking
- Printable reports

#### Data Upload
- Bulk import via CSV/Excel files
- Support for expenses, income, and department data
- Upload history and processing status
- Error handling and validation

## File Upload Formats

### Expense Data (CSV/Excel)
Required columns: `department_id`, `expense_type`, `amount`, `date`
```
department_id,expense_type,amount,date
1,Medical Supplies,5000.00,2024-01-15
2,Equipment Maintenance,2500.00,2024-01-16
```

### Income Data (CSV/Excel)
Required columns: `department_id`, `service_type`, `amount`, `date`
```
department_id,service_type,amount,date
1,Consultation,2500.00,2024-01-15
2,Surgery,15000.00,2024-01-16
```

### Department Data (CSV/Excel)
Required columns: `name`
```
name
Cardiology
Radiology
Pharmacy
```

## Project Structure

```
arthsutra/
├── accounts/          # User authentication & profiles
├── finance/           # Financial models & operations
├── reports/           # Dashboard & reporting
├── uploads/           # File upload & processing
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── arthsutra/        # Django settings & URLs
└── manage.py         # Django management script
```

## API Endpoints

- `/` - Dashboard (login required)
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/finance/expense/` - Add expense
- `/finance/income/` - Add income
- `/finance/loan/` - Add loan
- `/finance/list/` - Finance overview
- `/reports/reports/` - Financial reports
- `/uploads/upload/` - File upload
- `/uploads/history/` - Upload history
- `/admin/` - Django admin (superuser only)

## Security Features

- CSRF protection on all forms
- User authentication required for all views
- SQL injection prevention via Django ORM
- Secure file upload handling
- Password hashing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

---

**ArthSutra** - Streamlining Healthcare Finance Management</content>
<parameter name="filePath">f:\Projects\Arthsutra\arthsutra\README.md