from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application
from jobs.models import Job
from .forms import ApplicationForm

@login_required
def api_applications(request):
    if request.user.role != 'CANDIDATE':
        messages.error(request, "Only candidates can apply.")
        return redirect('home')

    form = ApplicationForm()
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.candidate = request.user
            
            already_applied = Application.objects.filter(candidate=app.candidate, job=app.job).exists()
            if already_applied:
                messages.error(request, "You have already applied for this job.")
            else:
                app.save()
                messages.success(request, "Application submitted successfully!")
                
            return redirect('candidate_dashboard')

    return redirect('candidate_dashboard')

@login_required
def api_update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == "POST":
        if application.job.recruiter != request.user:
             messages.error(request, "Not authorized to update this status.")
             return redirect('recruiter_dashboard')
             
        new_status = request.POST.get('status')
        if new_status in ['ACCEPTED', 'REJECTED', 'PENDING']:
             application.status = new_status
             application.save()
             messages.success(request, f"Application {new_status.lower()} successfully.")
        else:
             messages.error(request, "Invalid status.")
             
    return redirect('recruiter_dashboard')
