from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    StudentProfileForm,
    CounselorProfileForm,
)
from .models import User, StudentProfile, CounselorProfile


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if request.user.user_type == "student":
            profile_form = StudentProfileForm(
                request.POST, instance=request.user.studentprofile
            )
        elif request.user.user_type == "counselor":
            profile_form = CounselorProfileForm(
                request.POST, instance=request.user.counselorprofile
            )
        else:
            profile_form = None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        if request.user.user_type == "student":
            profile_form = StudentProfileForm(instance=request.user.studentprofile)
        elif request.user.user_type == "counselor":
            profile_form = CounselorProfileForm(instance=request.user.counselorprofile)
        else:
            profile_form = None

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "users/profile.html", context)
