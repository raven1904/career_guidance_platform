from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    UserUpdateForm,
    StudentProfileForm,
    CounselorProfileForm,
)


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


def custom_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("dashboard")
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


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
