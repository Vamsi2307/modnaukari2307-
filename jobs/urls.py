from django.urls import path
from .views import api_jobs, api_job_detail

urlpatterns = [
    path('jobs/', api_jobs, name='api-jobs'),
    path('jobs/<int:pk>/', api_job_detail, name='api-job-detail'),
]
