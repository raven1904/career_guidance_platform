from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def recommendation_dashboard(request):
    return render(request, "recommendations/dashboard.html")


@login_required
def career_paths(request):
    return render(request, "recommendations/career_paths.html")


@login_required
def skill_gap_analysis(request):
    return render(request, "recommendations/skill_gap.html")
