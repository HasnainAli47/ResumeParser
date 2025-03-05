from django.db import models
import os
from django.utils.timezone import now

class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=now)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=[("user", "User"), ("assistant", "Assistant")])
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

def upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    return f'resumes/{base}_{instance.id}{ext}'

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)  # Raw OCR text

class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="personal_info")
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="education")
    degree = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    field = models.CharField(max_length=255, blank=True, null=True)  
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4, blank=True, null=True)

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Expert', 'Expert')])

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="work_experience")
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20)
    responsibilities = models.TextField(blank=True, null=True)  # Add this if needed

class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=255)
    issued_by = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)