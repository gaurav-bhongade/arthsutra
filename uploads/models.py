from django.db import models
from django.conf import settings

class UploadedFile(models.Model):
    FILE_TYPES = (
        ('EXPENSE', 'Expense Data'),
        ('INCOME', 'Income Data'),
        ('DEPARTMENT', 'Department Data'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploaded_documents/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    records_processed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.file_type} - {self.file.name}"
