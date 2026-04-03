from django.db import models
from django.conf import settings

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return f"{self.title} at {self.company}"
