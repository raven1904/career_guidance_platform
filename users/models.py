from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("counselor", "Career Counselor"),
        ("admin", "Administrator"),
    )

    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="student"
    )
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class StudentProfile(models.Model):
    EDUCATION_LEVELS = (
        ("high_school", "High School"),
        ("undergraduate", "Undergraduate"),
        ("graduate", "Graduate"),
        ("phd", "PhD"),
        ("working", "Working Professional"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education_level = models.CharField(
        max_length=20, choices=EDUCATION_LEVELS, blank=True
    )
    field_of_study = models.CharField(max_length=200, blank=True)
    university = models.CharField(max_length=200, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    career_goals = models.TextField(blank=True)

    def __str__(self):
        return f"Student Profile: {self.user.username}"


class CounselorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    qualifications = models.TextField(blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    hourly_rate = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Counselor Profile: {self.user.username}"
