import pandas as pd
from finance.models import Expense, Income, Department
from .models import UploadedFile
import logging

logger = logging.getLogger(__name__)

def process_expense_csv(file_path, uploaded_file):
    """Process expense CSV/Excel file"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Expected columns: department_id, expense_type, amount, date
        required_columns = ['department_id', 'expense_type', 'amount', 'date']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")

        processed_count = 0
        skipped_count = 0
        for _, row in df.iterrows():
            try:
                # Check if department exists
                department_id = int(row['department_id'])
                if not Department.objects.filter(id=department_id).exists():
                    logger.warning(f"Department with ID {department_id} does not exist, skipping expense row")
                    skipped_count += 1
                    continue

                Expense.objects.create(
                    department_id=department_id,
                    expense_type=str(row['expense_type']),
                    amount=float(row['amount']),
                    date=pd.to_datetime(row['date']).date()
                )
                processed_count += 1
            except Exception as e:
                logger.error(f"Error processing expense row: {e}")
                skipped_count += 1
                continue

        uploaded_file.records_processed = processed_count
        uploaded_file.processed = True
        uploaded_file.save()

        if skipped_count > 0:
            logger.warning(f"Skipped {skipped_count} expense rows due to errors")

        return processed_count

    except Exception as e:
        logger.error(f"Error processing expense file: {e}")
        uploaded_file.processed = False
        uploaded_file.save()
        raise

def process_income_csv(file_path, uploaded_file):
    """Process income CSV/Excel file"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Expected columns: department_id, service_type, amount, date
        required_columns = ['department_id', 'service_type', 'amount', 'date']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")

        processed_count = 0
        skipped_count = 0
        for _, row in df.iterrows():
            try:
                # Check if department exists
                department_id = int(row['department_id'])
                if not Department.objects.filter(id=department_id).exists():
                    logger.warning(f"Department with ID {department_id} does not exist, skipping income row")
                    skipped_count += 1
                    continue

                Income.objects.create(
                    department_id=department_id,
                    service_type=str(row['service_type']),
                    amount=float(row['amount']),
                    date=pd.to_datetime(row['date']).date()
                )
                processed_count += 1
            except Exception as e:
                logger.error(f"Error processing income row: {e}")
                skipped_count += 1
                continue

        uploaded_file.records_processed = processed_count
        uploaded_file.processed = True
        uploaded_file.save()

        if skipped_count > 0:
            logger.warning(f"Skipped {skipped_count} income rows due to errors")

        return processed_count

    except Exception as e:
        logger.error(f"Error processing income file: {e}")
        uploaded_file.processed = False
        uploaded_file.save()
        raise

def process_department_csv(file_path, uploaded_file):
    """Process department CSV/Excel file"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Expected columns: name
        if 'name' not in df.columns:
            raise ValueError("Missing required column: name")

        processed_count = 0
        for _, row in df.iterrows():
            try:
                Department.objects.get_or_create(name=str(row['name']))
                processed_count += 1
            except Exception as e:
                logger.error(f"Error processing department row: {e}")
                continue

        uploaded_file.records_processed = processed_count
        uploaded_file.processed = True
        uploaded_file.save()

        return processed_count

    except Exception as e:
        logger.error(f"Error processing department file: {e}")
        uploaded_file.processed = False
        uploaded_file.save()
        raise
