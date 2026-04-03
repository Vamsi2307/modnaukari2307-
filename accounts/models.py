from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('RECRUITER', 'Recruiter'),
        ('CANDIDATE', 'Candidate'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CANDIDATE')

    def is_recruiter(self):
        return self.role == 'RECRUITER'

    def is_candidate(self):
        return self.role == 'CANDIDATE'
