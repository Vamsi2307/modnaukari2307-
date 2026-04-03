from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'recruiter', 'posted_at')
    list_filter = ('company', 'location', 'posted_at')
    search_fields = ('title', 'company', 'description')
