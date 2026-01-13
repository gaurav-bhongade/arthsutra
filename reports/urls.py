from django.urls import path
from .views import dashboard, reports_view

urlpatterns = [
    path('', dashboard, name='reports'),
    path('reports/', reports_view, name='reports_view'),
]
