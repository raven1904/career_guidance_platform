from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def learning_dashboard(request):
    return render(request, "learning/dashboard.html")


@login_required
def course_recommendations(request):
    return render(request, "learning/courses.html")


@login_required
def learning_paths(request):
    return render(request, "learning/paths.html")
