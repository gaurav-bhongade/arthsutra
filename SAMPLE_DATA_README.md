# Sample CSV Files for ArthSutra Healthcare Finance Management

This directory contains sample CSV files that you can use to test the bulk upload functionality in the ArthSutra system.

## 📁 Available Sample Files

### CSV Files (Recommended)
- `sample_expense_data.csv` - Healthcare expense records
- `sample_income_data.csv` - Healthcare income/service records  
- `sample_department_data.csv` - Department creation data

### Excel Files (.xlsx)
- `sample_expense_data.xlsx` - Healthcare expense records
- `sample_income_data.xlsx` - Healthcare income/service records
- `sample_department_data.xlsx` - Department creation data

## 🚀 How to Use

### Step 1: Access the Upload Page
1. Login to ArthSutra with admin credentials
2. Navigate to the "Upload" section from the sidebar
3. Click on "Upload Data" or "New Upload"

### Step 2: Upload Department Data First
1. Select "Department Data" as the file type
2. Choose `sample_department_data.csv` or `sample_department_data.xlsx`
3. Click "Upload & Process"
4. This will create the department records needed for expense/income uploads

### Step 3: Upload Expense Data
1. Select "Expense Data" as the file type
2. Choose `sample_expense_data.csv` or `sample_expense_data.xlsx`
3. Click "Upload & Process"
4. System will process and add expense records

### Step 4: Upload Income Data
1. Select "Income Data" as the file type
2. Choose `sample_income_data.csv` or `sample_income_data.xlsx`
3. Click "Upload & Process"
4. System will process and add income records

### Step 5: Verify Uploads
1. Go to "Upload History" to see processing status
2. Check Dashboard for updated financial summaries
3. Visit Reports page to see department-wise analytics

## 📊 Expected Results After Upload

### Financial Summary (Approximate)
- **Total Income**: ₹572,000
- **Total Expenses**: ₹315,000
- **Net Profit**: ₹257,000

### Department Performance
- **Cardiology**: High-value surgeries and consultations
- **Radiology**: Diagnostic imaging services
- **Pharmacy**: Medicine sales and supplies
- **Emergency**: Critical care treatments
- **Surgery**: Surgical procedures
- **Pediatrics**: Child healthcare services

## ⚠️ Important Notes

### Department ID Mapping
The sample expense and income files reference department IDs:
- 1: Cardiology
- 2: Radiology
- 3: Pharmacy
- 4: Emergency
- 5: Surgery
- 6: Pediatrics

### Date Format
All dates are in YYYY-MM-DD format (ISO 8601 standard)

### Data Validation
- Department IDs must exist before uploading expenses/incomes
- Amounts should be positive decimal numbers
- Dates should be valid and in the past/future as appropriate

### File Format Requirements
- CSV: UTF-8 encoding, comma-separated values
- Excel: .xlsx format (Excel 2007+)
- First row must contain column headers
- No empty rows or missing values

## 🧪 Testing Scenarios

### Successful Upload
- Use the provided sample files
- Ensure departments are created first
- Check upload history for "Processed" status

### Error Scenarios
- Try uploading expenses before departments (should fail)
- Upload file with wrong column names
- Upload file with invalid dates or amounts

### Large Data Testing
- Duplicate the sample data rows to create larger files
- Test system performance with 100+ records
- Verify processing time and memory usage

## 📈 Next Steps

After successful uploads:
1. **Dashboard**: View updated financial metrics
2. **Reports**: Analyze department performance
3. **Finance List**: Browse individual transactions
4. **Export**: Generate reports for stakeholders

## 🆘 Troubleshooting

### Common Issues
- **"Department not found"**: Upload department data first
- **"Invalid file format"**: Ensure CSV format and correct headers
- **"Processing failed"**: Check file encoding and data types

### Support
- Check upload history for detailed error messages
- Verify file format matches specifications
- Ensure database connectivity

---

**ArthSutra Sample Data** - Ready for testing and demonstration! 🏥📊</content>
<parameter name="filePath">f:\Projects\Arthsutra\arthsutra\SAMPLE_DATA_README.md