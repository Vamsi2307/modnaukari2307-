from django.urls import path
from .views import api_applications, api_update_application_status

urlpatterns = [
    path('applications/', api_applications, name='api-applications'),
    path('applications/<int:pk>/update_status/', api_update_application_status, name='api-update-application-status'),
]
