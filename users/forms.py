from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, StudentProfile, CounselorProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "user_type", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Create profile based on user type
            if user.user_type == "student":
                StudentProfile.objects.create(user=user)
            elif user.user_type == "counselor":
                CounselorProfile.objects.create(user=user)
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "bio",
            "profile_picture",
        ]


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            "education_level",
            "field_of_study",
            "university",
            "graduation_year",
            "skills",
            "interests",
            "career_goals",
        ]


class CounselorProfileForm(forms.ModelForm):
    class Meta:
        model = CounselorProfile
        fields = [
            "specialization",
            "experience_years",
            "qualifications",
            "license_number",
            "hourly_rate",
        ]
