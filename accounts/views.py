from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserRegisterForm
from .models import CustomUser

# -------------------- MAIN PAGES --------------------

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'RECRUITER':
            return redirect('recruiter_dashboard')
        else:
            return redirect('candidate_dashboard')
            
    from jobs.models import Job
    jobs = Job.objects.all().order_by('-posted_at')[:6]
    return render(request, 'home.html', {'jobs': jobs})

# -------------------- LOGIN / LOGOUT --------------------

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

# -------------------- REGISTER --------------------

def register_view(request):
    form = CustomUserRegisterForm()

    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = user.username
            email = user.email
            
            # Send Notification Email
            role_label = 'Recruiter' if user.role == 'RECRUITER' else 'Candidate'
            subject = f"Welcome to Naukari Job Portal, {username}!"
            message = (
                f"Hi {username},\n\n"
                f"Thank you for registering on Naukari Job Portal as a {role_label}.\n\n"
                f"You can now log in to your dashboard.\n\n"
                f"Best regards,\n"
                f"The Naukari Team"
            )
            try:
                send_mail(
                    subject,
                    message,
                    'no-reply@naukari.dummy',
                    [email],
                    fail_silently=True,
                )
            except Exception as e:
                pass

            messages.success(request, "Registration successful!")
            return redirect("login")

    return render(request, "register.html", {"form": form})

from jobs.models import Job
from applications.models import Application

# -------------------- DASHBOARDS --------------------

@login_required
def recruiter_dashboard(request):
    if request.user.role != 'RECRUITER':
        return redirect('home')
        
    jobs = Job.objects.filter(recruiter=request.user).order_by('-posted_at')
    applications = Application.objects.filter(job__recruiter=request.user).order_by('-applied_at')
    
    context = {
        'jobs': jobs,
        'applications': applications
    }
    return render(request, 'recruiter_dashboard.html', context)

@login_required
def candidate_dashboard(request):
    if request.user.role != 'CANDIDATE':
        return redirect('home')
        
    jobs = Job.objects.all().order_by('-posted_at')
    applications = Application.objects.filter(candidate=request.user).order_by('-applied_at')
    
    context = {
        'jobs': jobs,
        'my_applications': applications
    }
    return render(request, 'candidate_dashboard.html', context)
