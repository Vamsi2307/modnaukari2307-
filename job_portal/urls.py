from django.contrib import admin
from django.urls import path
from accounts.views import login_view, register_view, logout_user, home_view, recruiter_dashboard, candidate_dashboard
from jobs.views import api_jobs, api_job_detail
from applications.views import api_applications, api_update_application_status

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_view, name='register'),
    
    # Dashboards
    path('recruiter-dashboard/', recruiter_dashboard, name='recruiter_dashboard'),
    path('candidate-dashboard/', candidate_dashboard, name='candidate_dashboard'),
    
    # Internal Handlers
    path('jobs/post/', api_jobs, name='api-jobs'),
    path('jobs/<int:pk>/delete/', api_job_detail, name='api-job-detail'),
    path('applications/apply/', api_applications, name='api-applications'),
    path('applications/<int:pk>/status/', api_update_application_status, name='api-update-application-status'),
]
