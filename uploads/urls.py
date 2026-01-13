from django.urls import path
from .views import upload_file, upload_history

urlpatterns = [
    path('upload/', upload_file, name='upload'),
    path('history/', upload_history, name='upload_history'),
]
