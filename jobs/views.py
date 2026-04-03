from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .forms import JobForm
from applications.models import Application

@login_required
def api_jobs(request):
    if request.user.role != 'RECRUITER':
        messages.error(request, "Only recruiters can post jobs.")
        return redirect('home')

    form = JobForm()
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.recruiter = request.user
            new_job.save()
            messages.success(request, "Job created successfully!")
            return redirect('recruiter_dashboard')

    return render(request, "post_job.html", {"form": form})

@login_required
def api_job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == "POST" and request.POST.get('_method') == 'DELETE':
        if job.recruiter != request.user:
            messages.error(request, "Not authorized to delete this job.")
            return redirect('recruiter_dashboard')
            
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect('recruiter_dashboard')

    return redirect('recruiter_dashboard')
